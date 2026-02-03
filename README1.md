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
   │      └── usa app, db, bcrypt de __init__; forms e models; define rotas
   │
   └── myposts/forms.py
          └── usa Usuario de models (validação de email)
```

- **main.py** → ponto de entrada; só importa o `app` do pacote `myposts` e inicia o servidor.
- **myposts/__init__.py** → central: cria a aplicação, o banco e as extensões; depois importa `models` e `routes` para que as tabelas existam e as rotas sejam registradas.
- **myposts/models.py** → define os modelos (tabelas) e usa `db` e `login_manager` do `__init__`.
- **myposts/routes.py** → define as URLs e usa `app`, `db`, `bcrypt`, `forms` e `models`.
- **myposts/forms.py** → define formulários e usa o modelo `Usuario` para validações (ex.: email único).

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

Ou seja: a conexão entre os arquivos é por **importação de módulos** (Python). O `__init__.py` é o núcleo que expõe `app`, `db`, `bcrypt` e `login_manager` e garante que modelos e rotas estejam carregados na ordem correta.

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

## 4. Resumo para o usuário

- Os arquivos se conectam por **importação**: `main.py` só sobe o servidor; o resto vive no pacote `myposts`, com `__init__.py` no centro.
- O banco é acessado via **SQLAlchemy** (SQLite ou `DATABASE_URL`).
- Existem **duas tabelas**: `usuario` (quem faz login e cria posts) e `post` (título, corpo, data e autor), ligadas por **chave estrangeira** em uma relação **1:N** (um usuário, vários posts).
