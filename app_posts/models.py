from app_posts import db as database
from datetime import datetime

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    ## criando o relacionamento 1 para muitos entre Usuario e Post
    ## lazy=True significa que os posts so carregados quando acessados
    ## backref cria um atributo 'autor' em Post para acessar o Usuario associado
    posts = database.relationship('Post', backref='autor', lazy=True)
    curso = database.Column(database.String, nullable=False, default='Não informado')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
##  DEPRECATED -->  data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)

    ## criando a chave estrangeira para o relacionamento com Usuario
    ## 'usuario.id' referencia a tabela Usuario e sua coluna id e TEM QUE SER MINUSCULO
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)