from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import Usuario
from flask_login import current_user

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

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    curso_excel = BooleanField('Excel Impressionador')    
    curso_vba = BooleanField('VBA Impressionador')    
    curso_powerbi = BooleanField('Power BI Impressionador')    
    curso_ppt = BooleanField('Power Point Impressionador')    
    curso_python = BooleanField('Python Impressionador')    
    curso_sql = BooleanField('SQL Impressionador')    
    
    botao_submit_editarperfil = SubmitField('Confirmar Edição')
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já cadastrado. Utilize outro email.')