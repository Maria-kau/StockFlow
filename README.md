# StockFlow | API REST de Gerenciamento de Estoque

API REST desenvolvida com Python e Django REST Framework para gerenciamento de produtos, controle de estoque e registro de movimentações.

## Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- SQLite
- Git e GitHub
- Render
- Neon

## Funcionalidades

- Cadastro, consulta e atualização de produtos.
- Pesquisa e filtragem de produtos.
- Exclusão lógica e recuperação de produtos.
- Controle de entradas e saídas de estoque.
- Validação de movimentações.
- Histórico de movimentações.
- Identificação dos usuários responsáveis pelas operações.
- Autenticação e controle de permissões.

## Arquitetura

O projeto utiliza Django REST Framework para disponibilizar endpoints REST, PostgreSQL para persistência dos dados e autenticação baseada em tokens.

## Aplicação em produção

**API:** https://stockflow-xykg.onrender.com/

**Endpoint de produtos:** https://stockflow-xykg.onrender.com/api/products/

## Execução local

1. Clone o repositório:

   `git clone https://github.com/Maria-kau/StockFlow.git`

2. Instale as dependências:

   `pip install -r requirements.txt`

3. Configure as variáveis de ambiente no arquivo `.env`.

4. Execute as migrações:

   `python manage.py migrate`

5. Inicie o servidor:

   `python manage.py runserver`

## Testes

Execute os testes automatizados com:

`python manage.py test`

## Objetivo

Projeto desenvolvido para aplicar conceitos de desenvolvimento back-end, construção de APIs REST, regras de negócio, autenticação, controle de acesso e gerenciamento de banco de dados.

---

**Desenvolvido por Maria Kauellene**

[GitHub](https://github.com/Maria-kau)
