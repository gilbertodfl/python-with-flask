from flask import render_template, request, flash, redirect, url_for
from myposts import app, db, bcrypt
from myposts.forms import FormCriarConta, FormLogin
from myposts.models import Usuario, Post


#enquanto o banco não estiver em uso, vamos usar a lista fixa.
lista_usuarios = [ 'gilberto', 'samuel', 'joão' ]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

## Observe que por padrão o get é o método aceito por uma rota.
## Para aceitar o post, é necessário especificar o parâmetro methods na rota.

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login realizado com sucesso!{form_login.email.data}', 'alert-success')
        ##print(f'Login com o email: {form_login.email.data} e senha: {form_login.password.data} e lembrar de mim: {form_login.remember_me.data}')
        return ( redirect(url_for('home')) )
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_criptografada = bcrypt.generate_password_hash(form_criar_conta.password.data).decode('utf-8')
        usuario = Usuario(username=form_criar_conta.username.data,
                          email=form_criar_conta.email.data,
                          senha=senha_criptografada)
        # Adiciona o novo usuário ao banco de dados
        
        db.session.add(usuario)
        db.session.commit()

        flash(f'Conta criada com sucesso!{form_criar_conta.email.data}', 'alert-success')
        
        ##print(f'Criar conta com o username: {form_criar_conta.username.data}, email: {form_criar_conta.email.data} e senha: {form_criar_conta.password.data}')
        return ( redirect(url_for('home')) )
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
    
