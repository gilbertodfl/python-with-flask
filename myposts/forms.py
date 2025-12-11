from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import Usuario

class FormCriarConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    checkpassword = PasswordField('rewrite Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    botao_submit_criar_conta = SubmitField('Criar conta')

    ## verificação personalizada para garantir que o email não esteja cadastrado
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Utilize outro email.')

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=20)])
    remember_me = BooleanField('Remember Me')    
    botao_submit_login = SubmitField('Login')    

    # caso queira as mensagens em portguês, poderia usar o exemplo abaixo:
    #   validators=[
    #         DataRequired(message='Por favor, preencha o nome de usuário.')
    #     ])
    
    # email = StringField('Email', 
    #     validators=[
    #         DataRequired(message='Por favor, preencha o email.'),
    #         Email(message='Email inválido. Digite um email válido.')
    #     ])
    
    # password = PasswordField('Password', 
    #     validators=[
    #         DataRequired(message='Por favor, preencha a senha.'),
    #         Length(min=6, max=20, message='A senha deve ter entre 6 e 20 caracteres.')
    #     ])