from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm
from app.models import Org, Tag

ggm = Blueprint('main', __name__)

@ggm.route('/')
@ggm.route('/list')
def list():
    # only display published organizations on the orgslist page
    organizations = Org.query.filter_by(published=True).all()
    tags = Tag.query.all()

    return render_template('list.html', organizations=organizations, tags=tags)

@ggm.route('/Adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.list'))
    
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
