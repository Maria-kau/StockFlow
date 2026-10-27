
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import StockMovementSerializer
from .models import StockMovement
from products.models import Product


class StockEntryView(APIView):
    """View responsável por registrar entradas de estoque."""

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        # Valida o ID antes de consultar o banco.
        try:
            product_id = int(product_id)

            if isinstance(request.data.get("product_id"), bool):
                raise ValueError

            if str(product_id) != str(request.data.get("product_id")).strip():
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {"error": "ID do produto inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Bloqueia o registro durante a operação, em bancos compatíveis.
        product = Product.objects.select_for_update().filter(
            id=product_id
        ).first()

        if product is None:
            return Response(
                {"error": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if product.is_deleted:
            return Response(
                {"error": "Não é possível movimentar um produto na lixeira."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Valida a quantidade sem aceitar decimais ou booleanos.
        if isinstance(quantity, bool):
            return Response(
                {"error": "Informe uma quantidade inteira positiva."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            original_quantity = str(quantity).strip()
            quantity = int(quantity)

            if str(quantity) != original_quantity:
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {"error": "Informe uma quantidade inteira positiva."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return Response(
                {"error": "A quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Atualiza o estoque e registra a movimentação.
        product.stock += quantity
        product.save(update_fields=["stock"])

        user = request.user if request.user.is_authenticated else None

        StockMovement.objects.create(
            product=product,
            movement_type="IN",
            quantity=quantity,
            created_by=user,
        )

        return Response(
            {
                "message": "Entrada de estoque registrada com sucesso.",
                "product_id": product.id,
                "product_name": product.name,
                "quantity_added": quantity,
                "current_stock": product.stock,
            },
            status=status.HTTP_201_CREATED,
        )


class StockExitView(APIView):
    """View responsável por registrar saídas de estoque."""

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        # Valida o ID do produto.
        try:
            if isinstance(product_id, bool):
                raise ValueError

            original_product_id = str(product_id).strip()
            product_id = int(product_id)

            if str(product_id) != original_product_id:
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {"error": "ID do produto inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = Product.objects.select_for_update().filter(
            id=product_id
        ).first()

        if product is None:
            return Response(
                {"error": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if product.is_deleted:
            return Response(
                {"error": "Não é possível movimentar um produto na lixeira."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Valida a quantidade.
        if isinstance(quantity, bool):
            return Response(
                {"error": "Informe uma quantidade inteira positiva."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            original_quantity = str(quantity).strip()
            quantity = int(quantity)

            if str(quantity) != original_quantity:
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {"error": "Informe uma quantidade inteira positiva."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return Response(
                {"error": "A quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.stock < quantity:
            return Response(
                {
                    "error": (
                        "Estoque insuficiente para a saída. "
                        f"Estoque atual: {product.stock}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.stock -= quantity
        product.save(update_fields=["stock"])

        user = request.user if request.user.is_authenticated else None

        StockMovement.objects.create(
            product=product,
            movement_type="OUT",
            quantity=quantity,
            created_by=user,
        )

        return Response(
            {
                "message": "Saída de estoque registrada com sucesso.",
                "product_id": product.id,
                "product_name": product.name,
                "quantity_removed": quantity,
                "current_stock": product.stock,
            },
            status=status.HTTP_200_OK,
        )


class MovementHistoryView(APIView):
    """View responsável por consultar o histórico de movimentações."""

    def get(self, request):
        movements = StockMovement.objects.all().order_by("-created_at")
        serializer = StockMovementSerializer(movements, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
