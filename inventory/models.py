
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class StockMovement(models.Model):
    # Tipos de movimentação disponíveis.
    MOVEMENT_CHOICES = [
        ("IN", "Entrada"),
        ("OUT", "Saída"),
    ]

    # Relaciona a movimentação ao produto.
    # PROTECT impede a exclusão física do produto
    # enquanto houver movimentações relacionadas.
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="movements",
    )

    # Tipo de movimentação: entrada ou saída.
    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_CHOICES,
    )

    # Quantidade de unidades movimentadas.
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    # Custo por unidade, opcional.
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    # Motivo da movimentação, opcional.
    reason = models.CharField(
        max_length=200,
        blank=True,
    )

    # Data e hora de criação do registro.
    created_at = models.DateTimeField(auto_now_add=True)

    # Usuário responsável pela movimentação.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )

    class Meta:
        # Exibe as movimentações mais recentes primeiro.
        ordering = ["-created_at"]

        # Nomes exibidos no Django Admin.
        verbose_name = "Movimentação de estoque"
        verbose_name_plural = "Movimentações de estoque"

    def __str__(self):
        return (
            f"{self.movement_type} - "
            f"{self.product.name} - "
            f"{self.quantity}"
        )
