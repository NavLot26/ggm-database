from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, URL

# Admin login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Form for creating/editing blog posts
class OrganizationForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    website = StringField('Website', validators=[Optional(), URL()])
    description = TextAreaField('Description', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    tags = SelectMultipleField('Tags', coerce=int) # choices will be set in the route
    submit = SubmitField('Submit')
