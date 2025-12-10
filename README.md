

# Criar ambiente virtual no linux
python3 -m venv .venv

# Ativar o ambiente
source .venv/bin/activate



## RODAR O PROJETO:

flask --app main.py --debug run


## criando formulários - flask-wtf

## https://flask-wtf.readthedocs.io/en/stable/

flask_wtf: usado para criar formulários no python. 
```
pip instal flask-wtf

## é bom instalar, pois era para vir junto, mas não está vindo: 
pip install email_validator


```
O formulário envolve 3 arquivos basicamente:

forms.py que tem as importações dos fields, regras e todos os campos - aqui é a classe

main.py que importa o forms, cria a variável  e passa para o html- aqui instância. 

templates/login.html que recebe a variável e usa no formulário. 



## criando token - segurança
vamos gerar um token na mão:
```
python3
Python 3.12.7 | packaged by Anaconda, Inc. | (main, Oct  4 2024, 13:27:36) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import secrets
>>> secrets.token_hex(16)
'84741a09e5e38f33ac7410686aa03a5d'
>>> 
exit
```
vamos colocar essa chave no main.py

Como é ambiente de teste, não tem problema publicar aqui:

```
app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'

Dentro de cada chamada em forms html, coloque a chave: 
   {{ form_login.csrf_token }}

```
## enviando mensagem para o usuário:

A forma de mandar mensagem é assim:   flash(f'Login realizado com sucesso!{form_login.email.data}', 'alert-success')
No entanto, veja o arquivo base.html que precisa dessa referência. 

```
@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login realizado com sucesso!{form_login.email.data}', 'alert-success')
        ##print(f'Login com o email: {form_login.email.data} e senha: {form_login.password.data} e lembrar de mim: {form_login.remember_me.data}')
        return ( redirect(url_for('home')) )
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        flash(f'Conta criada com sucesso!{form_criar_conta.email.data}', 'alert-success')
        
        ##print(f'Criar conta com o username: {form_criar_conta.username.data}, email: {form_criar_conta.email.data} e senha: {form_criar_conta.password.data}')
        return ( redirect(url_for('home')) )
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
```    
Para entender melhor leia o arquivo base.html

## criando database
```
pip install flask-sqlalchemy
```
no arquivo main.py inicialmente: vamos criar com o nome mydatabase.db
```
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
```
### como seria as tabelas?
crie o arquivo models.py
```
from main import database
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



class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
##  DEPRECATED -->  data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now.utcnow)

    ## criando a chave estrangeira para o relacionamento com Usuario
    ## 'usuario.id' referencia a tabela Usuario e sua coluna id e TEM QUE SER MINUSCULO
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    
```