from .serializers import StockMovementSerializer
# Importa o serializer que será usado para validar e serializar
# os dados de movimentação de estoque.
from rest_framework.views import APIView
# APIView permite criar views baseadas em classes no Django REST Framework.

from rest_framework.response import Response
# Response cria a resposta HTTP enviada ao cliente.

from rest_framework import status
# status fornece códigos HTTP, como 400, 404 e 201.

from django.db import transaction
# transaction.atomic garante que as operações no banco sejam
# confirmadas juntas ou revertidas juntas se ocorrer uma exceção.

from .models import StockMovement
# Modelo que registra o histórico de movimentações do estoque.

from products.models import Product
# Modelo que representa os produtos cadastrados.


class StockEntryView(APIView):
    # View responsável por registrar entradas de estoque.

    @transaction.atomic
    def post(self, request):
        # Recebe os dados enviados pelo cliente.
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        # Procura o produto pelo ID.
        product = Product.objects.filter(id=product_id).first()

        # Verifica se o produto existe.
        if product is None:
            return Response(
                {"error": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se a quantidade é um número inteiro.
        try:
            if isinstance(quantity, bool):
                raise ValueError

            quantity = int(quantity)

            # Evita aceitar valores como "2.5" ou "2.0".
            if str(quantity) != str(request.data.get("quantity")).strip():
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {"error": "Quantidade inválida. Informe um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A quantidade da entrada deve ser maior que zero.
        if quantity <= 0:
            return Response(
                {"error": "Quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Atualiza o estoque atual do produto.
        product.stock += quantity
        product.save(update_fields=["stock"])

        # Identifica o usuário, se estiver autenticado.
        user = request.user if request.user.is_authenticated else None

        # Registra a movimentação no histórico.
        StockMovement.objects.create(
            product=product,
            movement_type="IN",
            quantity=quantity,
            created_by=user
        )

        # Retorna uma resposta de sucesso.
        return Response(
            {
                "message": "Entrada de estoque registrada com sucesso.",
                "product_id": product.id,
                "product_name": product.name,
                "quantity_added": quantity,
                "current_stock": product.stock
            },
            status=status.HTTP_201_CREATED
        )


class StockExitView(APIView):

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        # 1. Verificar se o produto existe
        product = Product.objects.filter(id=product_id).first()

        if product is None:
            return Response(
                {"error": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Validar a quantidade
        if isinstance(quantity, bool):
            return Response(
                {"error": "Quantidade inválida. Informe um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)

        except (TypeError, ValueError):
            return Response(
                {"error": "Quantidade inválida. Informe um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Impedir quantidades iguais ou menores que zero
        if quantity <= 0:
            return Response(
                {"error": "A quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Verificar se há estoque suficiente
        if product.stock < quantity:
            return Response(
                {
                    "error": (
                        "Estoque insuficiente para a saída. "
                        f"Estoque atual: {product.stock}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Atualizar o estoque
        product.stock -= quantity
        product.save(update_fields=["stock"])

        # 6. Identificar o usuário autenticado
        user = request.user if request.user.is_authenticated else None

        # 7. Registrar a movimentação de saída
        StockMovement.objects.create(
            product=product,
            movement_type="OUT",
            quantity=quantity,
            created_by=user
        )

        # 8. Retornar a resposta da API
        return Response(
            {
                "message": "Saída de estoque registrada com sucesso.",
                "product_id": product.id,
                "product_name": product.name,
                "quantity_removed": quantity,
                "current_stock": product.stock,
            },
            status=status.HTTP_200_OK
        )


class MovementHistoryView(APIView):
    def get(self, request):

        # Recupera todo os registros de movimentação de estoque da
        # base de todos os produtos, ordenando do mais recente para o mais antigo.
        movements = StockMovement.objects.all().order_by("created_at")
        #converte os movimentos em formato JSON
        serializer = StockMovementSerializer(movements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
