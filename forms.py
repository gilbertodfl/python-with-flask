from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormCriarConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    checkpassword = PasswordField('rewrite Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    botao_submit_criar_conta = SubmitField('Criar conta')

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=20)])
    remember_me = BooleanField('Remember Me')    
    botao_submit_login = SubmitField('Login')    