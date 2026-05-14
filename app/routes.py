from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

from app.forms import LoginForm, OrganizationForm, TagSearchForm
from app.models import User, Org, Tag

ggm = Blueprint('main', __name__)

@ggm.route('/', methods=['GET', 'POST'])
@ggm.route('/list', methods=['GET', 'POST'])
def list():
    # only display published organizations on the orgslist page
    organizations = Org.query.filter_by(published=True).all()
    tags = Tag.query.all()
    form = TagSearchForm()
    return render_template('list.html', orgs=organizations, tags=tags, form=form)

@ggm.route('/Adminlogin', methods=['GET', 'POST'])
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
    
@ggm.route('/Adminlogout')
@login_required
def adminlogout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.list'))

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