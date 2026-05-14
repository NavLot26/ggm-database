from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

from app.forms import LoginForm, OrganizationForm, TagSearchForm
from app.models import Org, Tag

from flask import session

from sqlalchemy import func

# ggm = Blueprint('main', __name__)

# this is initizalized to be None on program startup allowing it to be cached globably but only intialized when the database actually exists 
include_cache = None
exclude_cache = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def list(): 
    form = TagSearchForm()
    # query the included ids from the saved state, if nothing is there, and empty list is used
    include_ids = [int(id) for id in session.get("include", [])]

    # we intialize the form data with the session data on get
    if request.method == "GET":
        form.include.data = include_ids

    # we update the session data to the form data on post 
    if form.validate_on_submit():
        session["include"] = form.include.data
        
        return redirect(url_for("list"))  # Fix bug with refresh interference and stuff 


    
    filtered = (
        db.session.query(Org)
        .filter(Org.published == True)
    )
    
    if include_ids:
        print(include_ids)
        filtered = filtered.filter(
            Org.tags.any(Tag.id.in_(include_ids))
        )

    filtered = filtered.all()

    print(filtered)

    return render_template('list.html', orgs=filtered, form=form)


@app.route('/Adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_list'))

    form = LoginForm()

    if form.validate_on_submit():
        # check if the user exists and the password is correct
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(current_user.password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.adminlogin'))
    
        login_user(user, remember = form.remember_me.data)
        flash('You have been logged in.', 'success')
        return redirect(url_for('main.list'))

    return render_template('admin_login.html', form=form)
    
@app.route('/Adminlogout')
@login_required
def adminlogout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.list'))

@app.route('/admin_list')
# this is the admin page that lists all the organizations and tags, it is only accessible to logged in users
@login_required
def admin_list():
    organizations = Org.query.all()
    tags = Tag.query.all()
    return render_template('admin_list.html', organizations=organizations, tags=tags)

@ggm.route('/suggest', methods=['GET', 'POST'])
def suggest():
    form = OrganizationForm()

    if form.validate_on_submit():
        org = Org(
            name=form.name.data,
            website=form.website.data,
            description=form.description.data,
            address1=form.address1.data,
            address2=form.address2.data,
            city=form.city.data,
            state=form.state.data,
            published=False
        )
        db.session.add(org)
        db.session.commit()
        flash('Organization suggestion submitted successfully.', 'success')
        return redirect(url_for('main.list'))

    return render_template('suggest.html', form=form)

@ggm.route('/admin_suggest', methods=['GET', 'POST'])
@login_required
def admin_suggest():
    form = OrganizationForm()

    if form.validate_on_submit():
        org = Org(
            name=form.name.data,
            website=form.website.data,
            description=form.description.data,
            address1=form.address1.data,
            address2=form.address2.data,
            city=form.city.data,
            state=form.state.data,
            published=True
        )
        db.session.add(org)
        db.session.commit()
        flash('Organization added successfully.', 'success')
        return redirect(url_for('main.admin_list'))

    return render_template('admin_suggest.html', form=form)

@ggm.route('/admin_edit/<int:org_id>', methods=['GET', 'POST'])
@login_required
def admin_edit(org_id):
    org = Org.query.get_or_404(org_id)
    form = OrganizationForm(obj=org)

    if form.validate_on_submit():
        form.populate_obj(org)
        db.session.commit()
        flash('Organization updated successfully.', 'success')
        return redirect(url_for('main.admin_list'))

    return render_template('admin_suggest.html', form=form, org=org)