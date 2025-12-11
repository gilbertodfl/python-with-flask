import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa do __init__.py local (mesmo diretório)
from __init__ import app, db
from models import Post

## rode no comando de linha: python3 insert_post.py
with app.app_context():
   
        post = Post(titulo='posto 3', corpo="corpo 3", id_usuario="1")
       
        db.session.add(post)
        db.session.commit()
        print("Post inserido com sucesso!")

with app.app_context():
    posts = Post.query.all()
    print("Lista de posts no banco de dados: observe que no segundo print, eu não fiz a pesquisa e consigo pegar os dados do autor")
    for post in posts:
        print(f'ID: {post.id}, Título: {post.titulo}, Corpo: {post.corpo}, Data de Criação: {post.data_criacao}, ID do Usuário: {post.id_usuario}') 
        print(f'Autor do Post: {post.autor.username}, Email do Autor: {post.autor.email}')
