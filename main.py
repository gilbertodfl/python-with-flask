from flask import Flask, render_template, url_for
from forms import FormCriarConta, FormLogin
## https://flask-wtf.readthedocs.io/en/stable/

## https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)

lista_usuarios = [ 'gilberto', 'samuel', 'joão' ]

app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'


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
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
    

## o app.run() inicia o servidor Flask e o modo debug=True permite que o servidor
## seja reiniciado automaticamente sempre que houver uma alteração no código-fonte
if __name__ == "__main__":
    app.run(debug=True)