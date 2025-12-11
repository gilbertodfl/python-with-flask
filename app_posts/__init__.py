## configuração inicial do projeto Flask

##from flask import Flask, render_template, url_for, request, flash, redirect
##from forms import FormCriarConta, FormLogin
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

## https://flask-wtf.readthedocs.io/en/stable/

## https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)



app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

## create the SQLAlchemy db instance
db = SQLAlchemy(app)

## as rotas e modelos foram movidos para o pacote app_posts
## precisam ser chamadas logo após a criação do app Flask
## portanto, não mude de lugar essa importação.
from app_posts import routes
    