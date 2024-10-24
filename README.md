# Dependências do Projeto

Este projeto utiliza uma série de bibliotecas e frameworks que facilitam o desenvolvimento e a manutenção. Abaixo, apresentamos uma visão geral de cada uma delas:

## 1. **FastAPI**
FastAPI é um moderno framework web para construir APIs com Python. É projetado para ser rápido e eficiente, aproveitando os recursos do Python moderno, como tipagem e async/await. Sua principal vantagem é a capacidade de criar APIs RESTful de forma simples e com validação automática de dados, o que melhora a experiência de desenvolvimento.

## 2. **SQLAlchemy**
SQLAlchemy é uma biblioteca de ORM (Object-Relational Mapping) que fornece uma interface para interagir com bancos de dados relacionais de forma mais intuitiva e Pythonic. Ele abstrai a complexidade das consultas SQL, permitindo que você trabalhe com objetos Python em vez de manipular diretamente as tabelas do banco de dados.

## 3. **Pydantic**
Pydantic é uma biblioteca que facilita a validação de dados e a configuração de modelos de dados em Python. Ela é amplamente utilizada em conjunto com o FastAPI para garantir que as entradas de dados nas APIs estejam no formato correto e atendam às restrições definidas pelos modelos, o que reduz erros e melhora a segurança do aplicativo.

## 4. **SQLModel**
SQLModel é uma biblioteca que combina as funcionalidades do SQLAlchemy com as vantagens da Pydantic. Ela permite que você crie modelos de dados que são tanto compatíveis com bancos de dados quanto com a validação de dados, simplificando o trabalho com dados persistentes.

## 5. **Uvicorn**
Uvicorn é um servidor ASGI (Asynchronous Server Gateway Interface) que é leve e de alto desempenho. Ele é ideal para servir aplicações web escritas em Python e é amplamente utilizado para rodar aplicativos FastAPI, aproveitando a capacidade de execução assíncrona do framework.

## 6. **Alembic**
Alembic é uma ferramenta de migração de banco de dados que funciona com o SQLAlchemy. Ela permite que você gerencie alterações na estrutura do banco de dados de forma organizada, criando e aplicando migrações para manter o esquema do banco de dados atualizado com as alterações no modelo de dados.

## 7. **Jinja2**
Jinja2 é um motor de template para Python que permite gerar arquivos de texto a partir de templates HTML. Ele é usado para criar interfaces web dinâmicas, permitindo que você separe a lógica do aplicativo da apresentação, facilitando a manutenção e a escalabilidade.

## 8. **Python-Multipart**
Python-Multipart é uma biblioteca que fornece suporte para o upload de arquivos em aplicações web. Ela é especialmente útil em projetos que precisam manipular formulários com campos de arquivos, como imagens ou documentos.
