from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

from app.forms import LoginForm, OrganizationForm, TagSearchForm
from app.models import Org, Tag

from flask import session

# ggm = Blueprint('main', __name__)

# this is initizalized to be None on program startup allowing it to be cached globably but only intialized when the database actually exists 
include_cache = None
exclude_cache = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def list():
 
    form = TagSearchForm(); 

    if form.validate_on_submit():
        # save the include and exclude data in the session dict, not the objects themsevles which are tied to the context
        session["include"] = form.include.data
        session["exclude"] = form.exclude.data 
    
    # init filter in and filter out now based on the session include and exclude objects, or blank if the session has not stored them yet
    filterin = session.get('include') or []
    filterout = session.get('exclude') or []


    # only display published organizations on the orgslist page
    organizations = Org.query.filter_by(published=True).all()
    

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

    return render_template('list.html', orgs=organizations, tags=form.tagsnames, form=form, filterin = filterin, filterout = filterout)
 
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
