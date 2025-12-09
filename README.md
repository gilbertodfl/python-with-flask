

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

```
app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'
```
