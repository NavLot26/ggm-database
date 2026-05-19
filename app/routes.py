from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

from app.forms import LoginForm, OrganizationForm, TagSearchForm
from app.models import Org, Tag

from flask import session

from sqlalchemy import func

ggm = Blueprint('main', __name__)



@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def list(): 

   
    form = TagSearchForm()

    if form.validate_on_submit():
        print("pushing to session")
        include_ids = form.include.data
        session["include"] = include_ids

    else: 
        print("Pulling from session")
        include_ids = session.get("include", [])
        form.include.data = include_ids


    filtered = (
        db.session.query(Org)
        .filter(Org.published == True)
        .filter(Org.tags.any(Tag.id.in_(include_ids)))
    )

    return render_template('list.html', orgs=filtered, form=form)

@app.route('/Adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_list'))

    form = LoginForm()

    if form.validate_on_submit():
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
@login_required
def admin_list():
    organizations = Org.query.all()
    tags = Tag.query.all()
    return render_template('admin_list.html', organizations=organizations, tags=tags)

@app.route('/admin_suggest', methods=['GET', 'POST'])
@login_required
def admin_suggest():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('admin_suggest.html')