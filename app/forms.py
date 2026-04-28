from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from SelectMultipleCheckboxesField import SelectMultipleCheckboxesField
from wtforms.validators import DataRequired, Optional, URL

# Admin login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TagSearchForm(FlaskForm):
    tags=["Direct Service", "Environmental", "Food Insecurity", "Housing Insecurity", "Animals", "Children", "Elderly", "Over 16", "Health/Medical"],
    include = SelectMultipleCheckboxesField(
        "Include tags:",
        choices = tags
    )
    include = SelectMultipleCheckboxesField(
        "Exclude tags:",
        choices = tags
    )
    submit = SubmitField("submit!")

# Form for creating/editing blog posts
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
