
from django.conf import settings
from django.db import models


class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ("IN", "Entrada"),
        ("OUT", "Saída"),
    ]
    # Model representa o registro de movimentação de estoque de produtos.

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="movements",
    )
    # Relaciona a movimentação ao produto.
    # PROTECT impede excluir um produto que tenha movimentações.

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_CHOICES,
    )
    # Tipo de movimentação: entrada ou saída.

    quantity = models.PositiveIntegerField()
    # Quantidade de unidades movimentadas.

    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    # Custo por unidade, opcional quando não for aplicável.

    reason = models.CharField(max_length=200, blank=True)
    # Motivo da movimentação, opcional.

    created_at = models.DateTimeField(auto_now_add=True)
    # Data e hora de criação do registro.

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )
    # Usuário responsável pela movimentação.

    def __str__(self):
        return (
            f"{self.movement_type} - "
            f"{self.product.name} - "
            f"{self.quantity}"
        )
