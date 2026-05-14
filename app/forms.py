from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, URL
from wtforms.widgets import CheckboxInput, ListWidget
from app import app, db
from app.models import Org, Tag


class SelectMultipleCheckboxesField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# Admin login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TagSearchForm(FlaskForm):
    # choices are initially set to be empty here, because they can only be initialized 
    include = SelectMultipleCheckboxesField("Include tags:", choices=[])
    submit = SubmitField("Filter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # from app.models import Tag 

        tags = Tag.query.all()

        self.include.choices = [(int(tag.id), tag.name) for tag in tags] # choices for SelectMultipleCheckboxesField expects id, name tuple 

        self.include.data = [int(tag.id) for tag in tags] # include all of the gags by default 


# Form for creating/editing blog posts
# TAGS ARE CURRENTLY HARDCODED. this must be fixed before completion
class OrganizationForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    tags=["Direct Service", "Environmental", "Food Insecurity", "Housing Insecurity", "Animals", "Children", "Elderly", "Over 16", "Health/Medical"],
    include = SelectMultipleCheckboxesField(
        "Include tags:",
        choices = tags
    )
    description = TextAreaField('Description', validators=[DataRequired()])
    address1 = TextAreaField('Address 1', validators=[DataRequired()])
    address2 = TextAreaField('Address 2')
    city = TextAreaField('City', validators=[DataRequired()])
    state = TextAreaField('State', validators=[DataRequired()])
    zipcode = TextAreaField('zipcode', validators=[DataRequired()])
    website = TextAreaField('website', validators=[DataRequired()])
    submit = SubmitField('Submit')
