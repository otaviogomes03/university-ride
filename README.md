# University Ride

Sistema de caronas universitárias desenvolvido em **Django**, com busca de caronas, pagamentos e cadastro de usuários.

## Como executar

É necessário ter Python e Django instalados.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

python -m pip install django
python manage.py migrate
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/cadastro/** para criar uma conta ou **http://127.0.0.1:8000/entrar/** para entrar. Após o cadastro, o usuário é autenticado e direcionado para **/busca/**.

## Cadastro

O cadastro solicita nome completo, e-mail, senha e confirmação. O e-mail é utilizado como username do modelo `User` padrão do Django (limite de 150 caracteres). A senha é validada pelos validadores configurados em `AUTH_PASSWORD_VALIDATORS` e armazenada utilizando o mecanismo de hash do Django. E-mails repetidos são rejeitados, e as páginas POST possuem proteção CSRF. O login e o logout utilizam o sistema de autenticação do Django.

## Testes

```bash
python manage.py test contas
```

**Observação:** a configuração padrão do repositório está em modo de desenvolvimento (incluindo `DEBUG=True` e uma `SECRET_KEY` fixa). Antes de publicar o sistema, configure variáveis de ambiente, hosts permitidos, HTTPS e outras opções de segurança, conforme as recomendações de implantação do Django.
