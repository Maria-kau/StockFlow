
from rest_framework.test import APITestCase
from rest_framework import status


class ProductListTest(APITestCase):

    def test_list_products_returns_200(self):
        # Lista os produtos e verifica se a resposta retorna HTTP 200.
        response = self.client.get('/api/products/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_product_returns_201(self):
        # Cria um produto e verifica se a resposta retorna HTTP 201.
        data = {
            "name": "Produto Teste",
            "description": "descrição do produto teste",
            "price": "10.99",
            "stock": 100,
            "active": True
        }

        response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(response.data['name'], 'Produto Teste')
        self.assertEqual(
            response.data['description'],
            'descrição do produto teste'
        )
        self.assertEqual(response.data['price'], '10.99')
        self.assertEqual(response.data['stock'], 100)
        self.assertEqual(response.data['active'], True)

    def test_create_product_with_negative_price_returns_400(self):
        # Tenta cadastrar um produto com preço negativo e verifica
        # se a API rejeita a requisição com HTTP 400.
        data = {
            "name": "Produto Teste",
            "description": "descrição do produto teste",
            "price": "-10.99",
            "stock": 100,
            "active": True
        }

        response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_product_with_negative_stock_returns_400(self):
        # Tenta cadastrar um produto com estoque negativo e verifica
        # se a API rejeita a requisição com HTTP 400.
        data = {
            "name": "Produto Teste",
            "description": "descrição do produto teste",
            "price": "10.99",
            "stock": -100,
            "active": True
        }

        response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_product_with_empty_name_returns_400(self):
        # Tenta cadastrar um produto sem nome e verifica
        # se a API rejeita a requisição com HTTP 400.
        data = {
            "name": "",
            "description": "descrição do produto teste",
            "price": "10.99",
            "stock": 100,
            "active": True
        }

        response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_get_existing_product_returns_200(self):
        # Cadastra um produto, consulta seu ID e verifica
        # se a API retorna os dados com HTTP 200.
        data = {
            "name": "Mouse Gamer",
            "description": "Mouse para teste",
            "price": "89.90",
            "stock": 10,
            "active": True
        }

        create_response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        product_id = create_response.data['id']

        response = self.client.get(
            f'/api/products/{product_id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['name'],
            'Mouse Gamer'
        )

    def test_get_non_existing_product_returns_404(self):
        # Consulta um produto inexistente e verifica
        # se a API retorna HTTP 404.
        response = self.client.get('/api/products/9999/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_update_product_returns_200(self):
        # Cadastra um produto, atualiza seus dados e verifica
        # se a API retorna HTTP 200.
        data = {
            "name": "Produto Teste",
            "description": "descrição do produto teste",
            "price": "10.99",
            "stock": 100,
            "active": True
        }

        create_response = self.client.post(
            '/api/products/',
            data,
            format='json'
        )

        product_id = create_response.data['id']

        update_data = {
            "name": "Produto Teste Atualizado",
            "description": "descrição do produto teste atualizada",
            "price": "15.99",
            "stock": 150,
            "active": False
        }

        response = self.client.put(
            f'/api/products/{product_id}/',
            update_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['name'],
            'Produto Teste Atualizado'
        )

    def test_filter_products_by_active_status(self):
        # Prepara os dados de um produto ativo.
        active_product_data = {
            "name": "produto ativo",
            "description": "produto ativo para o teste",
            "price": "20.00",
            "stock": 70,
            "active": True
        }

        # Prepara os dados de um produto inativo.
        inactive_product_data = {
            "name": "produto inativo",
            "description": "produto inativo para o teste",
            "price": "30.00",
            "stock": 50,
            "active": False
        }

        # Cadastra os produtos que serão usados no teste.
        self.client.post(
            '/api/products/',
            active_product_data,
            format='json'
        )
        self.client.post(
            '/api/products/',
            inactive_product_data,
            format='json'
        )

        # Filtra a listagem para retornar somente produtos ativos.
        response_active = self.client.get(
            '/api/products/?active=true'
        )

        self.assertEqual(
            response_active.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response_active.data['count'], 1)
        self.assertEqual(
            response_active.data['results'][0]['name'],
            'produto ativo'
        )

        # Filtra a listagem para retornar somente produtos inativos.
        response_inactive = self.client.get(
            '/api/products/?active=false'
        )

        self.assertEqual(
            response_inactive.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response_inactive.data['count'], 1)
        self.assertEqual(
            response_inactive.data['results'][0]['name'],
            'produto inativo'
        )

    def test_search_products_by_name(self):
        # Cadastra um produto para realizar a pesquisa.
        self.client.post(
            '/api/products/',
            {
                "name": "Teclado Gamer",
                "description": "Teclado mecânico",
                "price": "199.90",
                "stock": 10,
                "active": True
            },
            format='json'
        )

        # Pesquisa produtos pelo nome usando o parâmetro search.
        response = self.client.get(
            '/api/products/?search=Teclado'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Teclado Gamer'
        )
