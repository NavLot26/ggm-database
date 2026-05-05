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
    tagobjs = Tag.query.all()
    tags = []
    for tag in tagobjs:
        tags.append(tagobjs.name)
    form = TagSearchForm()

    filterin = []
    filterout = []

    for i in range(len(organizations)-1, -1, -1):   #really messy and non-optimized but i think functional code for list filtering
        valid = True
        for fin in filterin:
            found = False
            for tag in organizations[i].tags:
                if (tag.name == fin):
                    found = True
            if not found:
                valid = False
        for fout in filterout:
            found = False
            for tag in organizations[i].tags:
                if (tag.name == fout):
                    found = True
            if found:
                valid = False
        if not valid:
            organizations.pop(i)
    

    if form.validate_on_submit():
        filterin = form.include.data
        filterout = form.include.data
    return render_template('list.html', orgs=organizations, tags=tags, form=form, filterin = filterin, filterout = filterout)

@ggm.route('/Adminlogin', methods=['GET', 'POST'])
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
    
@ggm.route('/Adminlogout')
@login_required
def adminlogout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.list'))

@ggm.route('/admin_list')
@login_required
def admin_list():
    organizations = Org.query.all()
    tags = Tag.query.all()
    return render_template('admin_list.html', organizations=organizations, tags=tags)

@ggm.route('/admin_suggest', methods=['GET', 'POST'])
@login_required
def admin_suggest():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('admin_suggest.html')
