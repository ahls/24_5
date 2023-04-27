from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, IntegerField, SelectField, EmailField,TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("username",validators=[InputRequired(),Length(max=20)])
    password = PasswordField("password",validators=[InputRequired()])
    email = EmailField("email address",validators=[InputRequired(),Length(max=50)])
    first_name = StringField("first name",validators=[InputRequired(),Length(max=30)])
    last_name = StringField("last name",validators=[InputRequired(),Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField("username",validators=[InputRequired()])
    password = PasswordField("password",validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("title",validators=[InputRequired(),Length(max=100)])
    content = TextAreaField("content",validators=[InputRequired()])