

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
Para entender melho leia o arquivo base.html