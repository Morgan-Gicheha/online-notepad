from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    
    username = StringField('Username',validators=[DataRequired()])
    email= StringField("Email",validators=[DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("REGISTER")

class Login(FlaskForm):

    email = StringField("Email",validators=[DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("LOGIN")