from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo


class RegisterForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min = 4, max = 15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = 8)])
    fname = StringField('firstName', validators=[InputRequired()])
    lname = StringField('lastName', validators=[InputRequired()])
    
