
from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from inventory.models import StockMovement
from products.models import Product

from rest_framework import status
from rest_framework.test import APITestCase


class ProductListTest(APITestCase):

    def test_list_products_returns_200(self):
        # Verifica se a listagem retorna HTTP 200.
        response = self.client.get('/api/products/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_product_returns_201(self):
        # Verifica se um produto é criado corretamente.
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
        # Verifica se a API rejeita um preço negativo.
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
        # Verifica se a API rejeita estoque negativo.
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
        # Verifica se a API rejeita um nome vazio.
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
        # Cria e consulta um produto existente.
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
        # Verifica se um produto inexistente retorna HTTP 404.
        response = self.client.get('/api/products/9999/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_update_product_returns_200(self):
        # Cria e atualiza um produto.
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
        # Cria um produto ativo.
        active_product_data = {
            "name": "produto ativo",
            "description": "produto ativo para o teste",
            "price": "20.00",
            "stock": 70,
            "active": True
        }

        # Cria um produto inativo.
        inactive_product_data = {
            "name": "produto inativo",
            "description": "produto inativo para o teste",
            "price": "30.00",
            "stock": 50,
            "active": False
        }

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

        # Filtra somente os produtos ativos.
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

        # Filtra somente os produtos inativos.
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
        # Cria um produto para pesquisar pelo nome.
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

        # Pesquisa pelo nome usando o parâmetro search.
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

    def test_list_trash_products(self):
        # Cria um produto que não está na lixeira.
        Product.objects.create(
            name="pó banana",
            price="15.90",
            stock=8,
        )

        # Cria um produto que está na lixeira.
        Product.objects.create(
            name="rimel",
            price="12.90",
            stock=9,
            is_deleted=True,
            deleted_at=timezone.now(),
        )

        response = self.client.get('/api/products/trash/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'rimel'
        )

    def test_restore_product(self):
        # Cria um produto que está na lixeira.
        produto = Product.objects.create(
            name="Rímel",
            price="12.90",
            stock=9,
            is_deleted=True,
            deleted_at=timezone.now(),
        )

        # Solicita a restauração do produto.
        response = self.client.post(
            f'/api/products/{produto.id}/restore/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Atualiza o objeto com os dados atuais do banco.
        produto.refresh_from_db()

        # Verifica se o produto saiu da lixeira.
        self.assertFalse(produto.is_deleted)
        self.assertIsNone(produto.deleted_at)


class ProductTrashCommandTest(TestCase):

    def test_delete_expired_product(self):
        # Cria um produto na lixeira há mais de 30 dias.
        data_exclusao = timezone.now() - timedelta(days=31)

        produto = Product.objects.create(
            name="blush coral rose",
            description="blush compacto na cor coral rose",
            price="21.90",
            stock=10,
            is_deleted=True,
            deleted_at=data_exclusao
        )

        # Executa o comando de exclusão.
        call_command("delete_expired_products")

        # Verifica se o produto foi excluído.
        self.assertFalse(
            Product.objects.filter(id=produto.id).exists()
        )

    def test_preserve_product_with_movements(self):
        # Cria um produto antigo na lixeira.
        data_exclusao = timezone.now() - timedelta(days=31)

        produto = Product.objects.create(
            name="blush coral rose",
            description="blush compacto na cor coral rose",
            price="21.90",
            stock=10,
            is_deleted=True,
            deleted_at=data_exclusao
        )

        # Registra uma movimentação de estoque para o produto.
        StockMovement.objects.create(
            product=produto,
            movement_type="IN",
            quantity=5
        )

        # Executa o comando de exclusão.
        call_command("delete_expired_products")

        # Verifica se o produto foi preservado.
        self.assertTrue(
            Product.objects.filter(id=produto.id).exists()
        )


        
    def test_delete_product_moves_it_to_trash(self):
        # 1. Cria um produto pela API.
        response_create = self.client.post(
            '/api/products/',
            {
                "name": "Blush Rosa",
                "price": "19.90",
                "stock": 10
            },
            format='json'
        )

        # 2. Guarda o ID do produto criado.
        product_id = response_create.data['id']

        # 3. Envia a requisição para excluir o produto.
        response_delete = self.client.delete(
            f'/api/products/{product_id}/'
        )

        # 4. Verifica se a exclusão foi processada.
        self.assertEqual(
            response_delete.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # 5. Busca o produto diretamente no banco de dados.
        produto = Product.objects.get(id=product_id)

        # 6. Confirma que ele foi para a lixeira.
        self.assertTrue(produto.is_deleted)
        self.assertIsNotNone(produto.deleted_at)
