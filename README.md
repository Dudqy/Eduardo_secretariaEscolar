# 📚 Eduardo Secretaria Escolar

Sistema web desenvolvido com **Django** para gerenciar informações e processos administrativos de uma instituição escolar.  
O projeto permite o cadastro e gerenciamento de alunos, turmas, eventos e contratos, oferecendo uma interface organizada e funcional para controle interno da secretaria.

---

## 📑 Índice

- [Introdução](#-introdução)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Configuração](#-configuração)
- [Banco de Dados](#-banco-de-dados)
- [Testes](#-testes)
- [Contribuidores](#-contribuidores)
- [Licença](#-licença)

---

## 🚀 Introdução

O **Eduardo Secretaria Escolar** é um sistema administrativo voltado para a gestão de escolas, facilitando o controle de dados de alunos, professores e eventos escolares.  
Ele foi desenvolvido com o framework **Django**, aproveitando seu sistema de ORM, autenticação e painel administrativo.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Django 4.x**
- **SQLite3** (banco de dados padrão)
- **HTML / CSS / JavaScript**
- **Bootstrap** (para o layout administrativo)
- **Django Admin**

---

## 🗂 Estrutura do Projeto

```
Eduardo_secretariaEscolar/
│
├── Eduardo_secretariaEscolar/        # Configurações principais do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                             # App base (configurações e modelos principais)
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── secretariaescolar/                # App de funcionalidades da secretaria
│   ├── models.py
│   ├── validators.py
│   ├── views.py
│   ├── signals.py
│   └── urls.py
│
├── db.sqlite3                        # Banco de dados local
├── manage.py                         # CLI do Django
└── README.md
```

---

## ⚙️ Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/Dudqy/Eduardo_secretariaEscolar.git
   cd Eduardo_secretariaEscolar
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

   > Caso o arquivo `requirements.txt` não exista, você pode instalá-las manualmente:
   >
   > ```bash
   > pip install django
   > ```

4. **Realize as migrações do banco**

   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário**

   ```bash
   python manage.py createsuperuser
   ```

---

## ▶️ Como Executar

Inicie o servidor local do Django:

```bash
python manage.py runserver
```

Acesse no navegador:

```
http://127.0.0.1:8000/
```

Painel administrativo:

```
http://127.0.0.1:8000/admin/
```

---

## 🌟 Funcionalidades Principais

- 📋 Cadastro e gerenciamento de **alunos, turmas e contratos**
- 🧾 Controle de **eventos e ocorrências escolares**
- 🧑‍🏫 Sistema de **autenticação de usuários (Django Admin)**
- 📊 Interface administrativa com filtros e busca
- 🔔 Notificações via **signals** do Django
- 🗃 Integração com **SQLite3**

---

## ⚙️ Configuração

As principais configurações do sistema estão em:

```
Eduardo_secretariaEscolar/Eduardo_secretariaEscolar/settings.py
```

Você pode ajustar:
- Banco de dados (para PostgreSQL, MySQL, etc.)
- Idioma e timezone (`LANGUAGE_CODE` e `TIME_ZONE`)
- Configuração de apps instalados (`INSTALLED_APPS`)

---

## 🧠 Banco de Dados

O projeto utiliza **SQLite3** por padrão, localizado no arquivo `db.sqlite3`.

Para mudar o banco, edite `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'secretaria',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🧪 Testes

Execute os testes unitários com:

```bash
python manage.py test
```

---

## 👥 Contribuidores

- **Eduardo (Dudqy)** — Autor e desenvolvedor principal  
- Contribuições são bem-vindas! Para contribuir:
  1. Faça um *fork* do repositório  
  2. Crie uma *branch* (`git checkout -b feature/nome-da-feature`)  
  3. Faça *commit* das mudanças  
  4. Abra um *Pull Request*

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**.  
Você é livre para usar, modificar e distribuir o código, desde que mantenha os créditos originais.
