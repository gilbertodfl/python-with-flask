from flask import render_template, request, flash, redirect, url_for
from myposts import app, db, bcrypt
from myposts.forms import FormCriarConta, FormLogin, FormCriarConta, FormEditarPerfil
from myposts.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required

import secrets
import os
from PIL import Image

#enquanto o banco não estiver em uso, vamos usar a lista fixa.
lista_usuarios = [ 'gilberto', 'samuel', 'joão' ]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

## Observe que por padrão o get é o método aceito por uma rota.
## Para aceitar o post, é necessário especificar o parâmetro methods na rota.

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        ## checa se a senha está correta e bate com o hash armazenado no banco.
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.password.data):
            ## o login_user vem do flask_login e vai gerenciar a sessão do usuário. Inclusive cookies se "remember me" for marcado.
            login_user(usuario, remember=form_login.remember_me.data)
            flash(f'Login realizado com sucesso!{form_login.email.data}', 'alert-success')
            ##print(f'Login com o email: {form_login.email.data} e senha: {form_login.password.data} e lembrar de mim: {form_login.remember_me.data}')
            par_next = request.args.get('next')
            if par_next:
                return ( redirect(par_next) )
            else:   
                return ( redirect(url_for('home')) )
        else:
            flash('Falha no login. Email ou senha incorretos.', 'alert-danger')
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
    
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


## pegamos um modelopronto em: https://freefrontend.com/bootstrap-profiles/
## https://bbbootstrap.com/snippets/bootstrap-sidebar-user-profile-62301382

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    ## print(f'Nome do arquivo: {nome_arquivo} salvo com sucesso!')
    return nome_arquivo
def atualizar_curso(form):
    lista_curso = []
    for campo in form:
       if 'curso_' in campo.name:
        if campo.data:
            lista_curso.append(campo.label.text)
    return ';'.join(lista_curso)
    

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.curso = atualizar_curso(form)
        if current_user.curso == '':
            current_user.curso = 'Não informado'
        db.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/criar')  
@login_required 
def criar_post():
    return render_template('criarpost.html')