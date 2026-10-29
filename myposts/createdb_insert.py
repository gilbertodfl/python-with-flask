import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from myposts import app, db
from myposts.models import Usuario, Post

## MODO DE USO:
##  rode no comando de linha: 
##  garanta que está onde está o main.py
##  cd /home/gilberto/APRENDIZADO/HASHTAG/python impressionador/FLASK/flask-post-user/post-user
##  python -m myposts.createdb_insert
## aqui ficou como exemplo, mas veja que em __init__.py já estamos criando e abrindo. 

with app.app_context():
    # Criar tabelas. Se existir, NÃO SOBREPÕE!!.
    ## se precisar recriar, apague o arquivo com comando : rm instance/site.db        
    ## ou também poderia ter uma instrução antes do create_all: db.drop_all()
    db.create_all()
    print("Tabelas criadas!")
    
    # Verificar se já existem usuários antes de inserir
    if Usuario.query.count() == 0:

        usuario_teste = Usuario(username='gilberto', email="gilberto@gmail.com", senha="123456")
        usuario_teste2 = Usuario(username='gilberto2', email="gilberto2@gmail.com", senha="123456")
        usuario_teste3 = Usuario(username='gilberto3', email="gilberto3@gmail.com", senha="123456")
        db.session.add(usuario_teste)
        db.session.add(usuario_teste2)
        db.session.add(usuario_teste3)        
        db.session.commit()
        print("Usuários inseridos com sucesso!")
    else:
        print("Usuários já existem no banco!")

with app.app_context():
    usuarios = Usuario.query.all()
    print("Lista de usuários no banco de dados:" )
    for usuario in usuarios:
        print(f'ID: {usuario.id}, Username: {usuario.username}, Email: {usuario.email}')

with app.app_context():
    total_usuarios = Usuario.query.count()
    print(f'Total de usuários no banco de dados: {total_usuarios}') 
with app.app_context():
    usuario_especifico = Usuario.query.filter_by(username='gilberto2').first()
    if usuario_especifico:
        print(f'Usuário encontrado: ID: {usuario_especifico.id}, Username: {usuario_especifico.username}, Email: {usuario_especifico.email}')    

with app.app_context():
    usuario_especifico = Usuario.query.filter_by(username='gilberto2', senha='123456').first()
    print( "Buscando usuário com username 'gilberto2' e senha '123456'" )
    if usuario_especifico:
        print(f'Usuário encontrado: ID: {usuario_especifico.id}, Username: {usuario_especifico.username}, Email: {usuario_especifico.email}')
    else:
        print('Usuário não encontrado ou senha incorreta')        
with app.app_context():
    posts=Post.query.first()
    print ("Buscando o primeiro post no banco de dados")
    if posts:
        print(f'Post encontrado: ID: {posts.id}, Título: {posts.titulo}, Corpo: {posts.corpo}, Data de Criação: {posts.data_criacao}, ID do Usuário: {posts.id_usuario}')   