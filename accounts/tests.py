from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class LoginTests(APITestCase):

    def setUp(self):
        # Cria um usuário para utilizar nos testes
        self.user = User.objects.create_user(
            username="kau",
            password="SenhaForte123"
        )

    def test_login_com_credenciais_validas(self):
        # Envia usuário e senha para o endpoint de login
        response = self.client.post(
            "/api/accounts/login/",
            {
                "username": "kau",
                "password": "SenhaForte123"
            }
        )

        # Verifica se o login foi realizado com sucesso
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se a resposta contém um token
        self.assertIn("token", response.data)

        # Verifica se o token não está vazio
        self.assertTrue(response.data["token"])

