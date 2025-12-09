from flask import Flask, render_template

## https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)

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

## o app.run() inicia o servidor Flask e o modo debug=True permite que o servidor
## seja reiniciado automaticamente sempre que houver uma alteração no código-fonte
if __name__ == "__main__":
    app.run(debug=True)