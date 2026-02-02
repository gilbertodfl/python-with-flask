## configuração inicial do projeto Flask

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os 
## https://flask-wtf.readthedocs.io/en/stable/

## https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)

app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

## create the SQLAlchemy db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
## o login_view define qual função de rota vai ser chamada quando um usuário
## tentar acessar uma rota protegida sem estar logado.
## Observe que 'login' é o nome da função de rota definida em routes.py
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

## as rotas e modelos foram movidos para o pacote myposts
## precisam ser chamadas logo após a criação do app Flask
## portanto, não mude de lugar essa importação.

from . import routes
    