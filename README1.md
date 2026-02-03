# Documentação do Projeto — Visão Geral

Documentação sucinta para usuários: conexão entre arquivos, tipos de vínculo e tabelas do banco.

---

## 1. Conexão entre os arquivos

```
main.py
   └── importa app de myposts
          │
myposts/__init__.py
   ├── cria app Flask, db (SQLAlchemy), bcrypt, login_manager
   ├── importa models (para definir e criar tabelas)
   └── importa routes (registra rotas no app)
          │
   ├── myposts/models.py
   │      └── usa db e login_manager de __init__; define Usuario e Post
   │
   ├── myposts/routes.py
   │      └── usa app, db, bcrypt de __init__; forms e models; define rotas; renderiza templates
   │
   ├── myposts/forms.py
   │      └── usa Usuario de models (validação de email); define formulários da aplicação
   │
   └── myposts/templates/
          └── arquivos HTML (base, home, login, perfil, post, etc.) usados por render_template() nas rotas
```

- **main.py** → ponto de entrada; só importa o `app` do pacote `myposts` e inicia o servidor.
- **myposts/__init__.py** → central: cria a aplicação, o banco e as extensões; depois importa `models` e `routes` para que as tabelas existam e as rotas sejam registradas.
- **myposts/models.py** → define os modelos (tabelas) e usa `db` e `login_manager` do `__init__`.
- **myposts/routes.py** → define as URLs e usa `app`, `db`, `bcrypt`, `forms` e `models`; devolve as páginas usando **myposts/templates/** (HTML).
- **myposts/forms.py** → ver seção “Para que serve o forms.py” abaixo.
- **myposts/templates/** → pasta onde ficam os arquivos HTML da aplicação. O Flask procura os templates nessa pasta quando as rotas chamam `render_template()` (ex.: `home.html`, `login.html`, `perfil.html`, `post.html`, `usuarios.html`, `criarpost.html`, `editarperfil.html`, `contato.html`, `base.html`, `navbar.html`). Não há importação de Python: a conexão é pelo nome do arquivo passado para `render_template()` nas rotas.

---

## 2. Tipo de conexão

| De              | Para     | Tipo de conexão                          |
|-----------------|----------|------------------------------------------|
| main.py         | myposts  | **Importação**: usa o `app` do pacote    |
| __init__.py     | models   | **Importação**: carrega modelos e tabelas|
| __init__.py     | routes   | **Importação**: registra rotas no `app`  |
| models.py       | __init__ | **Importação**: usa `db` e `login_manager` |
| routes.py       | __init__ | **Importação**: usa `app`, `db`, `bcrypt`|
| routes.py       | forms    | **Importação**: usa formulários          |
| routes.py       | models   | **Importação**: usa `Usuario` e `Post`   |
| forms.py        | models   | **Importação**: usa `Usuario` (validação)|
| routes.py       | templates | **Uso em tempo de execução**: `render_template('nome.html', ...)` carrega HTML de `myposts/templates/` |

Ou seja: a conexão entre os arquivos é por **importação de módulos** (Python). A pasta **templates** é usada em tempo de execução pelas rotas, sem importação direta. O `__init__.py` é o núcleo que expõe `app`, `db`, `bcrypt` e `login_manager` e garante que modelos e rotas estejam carregados na ordem correta.

---

## 3. Banco de dados e tabelas

- **Conexão**: SQLAlchemy.
- **Driver/banco**: 
  - Em produção: valor de `DATABASE_URL` (ex.: PostgreSQL).
  - Sem `DATABASE_URL`: SQLite, arquivo `site.db` na raiz do projeto.

Tabelas criadas automaticamente (via `db.create_all()` no `__init__.py`):

### Tabela `usuario`

| Coluna      | Tipo        | Observação                          |
|------------|-------------|-------------------------------------|
| id         | Integer     | Chave primária                      |
| username   | String      | Obrigatório                         |
| email      | String      | Obrigatório, único                  |
| senha      | String      | Obrigatório (hash com Bcrypt)      |
| foto_perfil| String      | Padrão: `default.jpg`               |
| curso      | String      | Padrão: `Não informado`             |

### Tabela `post`

| Coluna      | Tipo        | Observação                          |
|------------|-------------|-------------------------------------|
| id         | Integer     | Chave primária                      |
| titulo     | String      | Obrigatório                         |
| corpo      | Text        | Obrigatório                         |
| data_criacao | DateTime  | Obrigatório, preenchido no cadastro |
| id_usuario | Integer     | Chave estrangeira → `usuario.id`    |

**Relacionamento:** um **usuário** pode ter **vários posts** (1:N). Em `Post`, o campo `id_usuario` referencia `usuario.id`; no modelo `Usuario`, a lista de posts é acessada por `usuario.posts` e, em `Post`, o autor por `post.autor`.

---

## 4. Para que serve o forms.py

O **forms.py** define os **formulários da aplicação** (Flask-WTF). Ele serve para:

- **Criar conta** (`FormCriarConta`): campos de username, email, senha e confirmação de senha; valida se o email já está cadastrado.
- **Login** (`FormLogin`): email, senha e “Lembrar de mim”; usado na tela de login.
- **Editar perfil** (`FormEditarPerfil`): username, email, foto de perfil e cursos (checkboxes); valida email único ao editar.
- **Criar/editar post** (`FormCriarPost`): título e corpo do post.

Cada formulário tem validações (obrigatório, email válido, tamanho da senha, etc.) e é usado em **routes.py**: as rotas instanciam o form, passam para o template e, no POST, usam `form.validate_on_submit()` e `form.campo.data` para processar os dados antes de gravar no banco. Ou seja: **forms.py** centraliza a definição e a validação dos dados que o usuário envia pelos formulários HTML.

### Relação do forms.py com models

O **forms.py** depende do **models.py** da seguinte forma:

- **Importação:** o `forms.py` importa o modelo `Usuario` de `models` (`from .models import Usuario`) e usa `current_user` do Flask-Login (que é uma instância de `Usuario` quando o usuário está logado).

- **Validação contra o banco:** os formulários usam o modelo para consultar o banco e validar regras de negócio:
  - **FormCriarConta:** no método `validate_email`, usa `Usuario.query.filter_by(email=email.data).first()` para garantir que o email ainda não esteja cadastrado; se já existir, retorna erro de validação.
  - **FormEditarPerfil:** no método `validate_email`, usa `Usuario.query.filter_by(email=email.data).first()` para garantir que, ao editar o email, o novo valor não pertença a outro usuário; se o email não mudou (`current_user.email == email.data`), a validação não consulta o banco.

- **Alinhamento com as tabelas:** os campos dos formulários espelham campos das tabelas (username, email, senha em usuário; título e corpo em post). O **forms.py** não grava no banco; ele só valida e entrega os dados. Quem cria ou atualiza registros é o **routes.py**, usando os modelos `Usuario` e `Post` e os dados já validados do form (por exemplo `form.username.data`, `form.email.data`).

Em resumo: **models** define a estrutura das tabelas e dos objetos; **forms** define a entrada do usuário e usa o modelo **Usuario** apenas para consultas de validação (email único). Os dados validados pelo form são depois usados nas rotas para criar ou atualizar instâncias de `Usuario` ou `Post`.

---

## 5. Resumo para o usuário

- Os arquivos se conectam por **importação**: `main.py` só sobe o servidor; o resto vive no pacote `myposts`, com `__init__.py` no centro.
- A pasta **myposts/templates/** guarda os HTMLs; as rotas usam `render_template('arquivo.html', ...)` para exibir as páginas.
- O **forms.py** serve para definir e validar os formulários (login, criar conta, editar perfil, criar/editar post); as rotas usam esses formulários para receber e validar dados do usuário. O **forms.py** se relaciona com o **models**: importa `Usuario` e o usa em validações (consultas ao banco para garantir email único); não grava no banco — quem grava são as rotas, usando os modelos e os dados já validados do form.
- O banco é acessado via **SQLAlchemy** (SQLite ou `DATABASE_URL`).
- Existem **duas tabelas**: `usuario` (quem faz login e cria posts) e `post` (título, corpo, data e autor), ligadas por **chave estrangeira** em uma relação **1:N** (um usuário, vários posts).
