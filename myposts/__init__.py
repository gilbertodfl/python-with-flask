## configuração inicial do projeto Flask

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy

import os 
from dotenv import load_dotenv

## https://flask-wtf.readthedocs.io/en/stable/

## https://flask.palletsprojects.com/en/stable/

load_dotenv()
app = Flask(__name__)

# --- CÓDIGO DE DIAGNÓSTICO ---
# print("--- Verificação do arquivo .env ---")
# variaveis_para_checar = ['SECRET_KEY', 'DATABASE_URL']

# for var in variaveis_para_checar:
#     valor = os.getenv(var)
#     if valor:
#         # Mostra os 4 primeiros caracteres por segurança, se quiser ver tudo use apenas {valor}
#         print(f"✅ {var} encontrada: {valor}...") 
#     else:
#         print(f"❌ {var} NÃO encontrada no ambiente.")
# print("-----------------------------------")
# Forçamos a leitura e já aplicamos
chave = os.getenv('SECRET_KEY')
if not chave:
    raise ValueError("A SECRET_KEY não foi encontrada no arquivo .env!")

app.config['SECRET_KEY'] = str(chave) # Força ser string por garantia

##app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'
# Pega o caminho absoluto da pasta onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))

# Tenta pegar a URL do .env
env_db_url = os.getenv('DATABASE_URL')

if env_db_url:
    # Se a URL no .env for SQLite, vamos garantir que ela aponte para o lugar certo
    if env_db_url.startswith("sqlite:///"):
        # Extrai apenas o nome do arquivo (site.db) e força o caminho absoluto
        db_name = env_db_url.split('/')[-1]
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", db_name)}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = env_db_url
else:
    # Caso não tenha nada no .env, usa o padrão seguro
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "site.db")}'

## create the SQLAlchemy db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
## o login_view define qual função de rota vai ser chamada quando um usuário
## tentar acessar uma rota protegida sem estar logado.
## Observe que 'login' é o nome da função de rota definida em routes.py
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

#criando o engine para o banco de dados
from myposts import models

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table('usuario'):
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tabelas criadas!")
else:
    print("Tabelas já existem!")
###########################################

## as rotas e modelos foram movidos para o pacote myposts
## precisam ser chamadas logo após a criação do app Flask
## portanto, não mude de lugar essa importação.

from . import routes
    