
from rest_framework import serializers
from .models import StockMovement


# created_at = criado_em / created_by = criado_por
class StockMovementSerializer(serializers.ModelSerializer):
    # Criamos uma classe que herda de ModelSerializer,
    # uma classe do Django REST Framework para serializar modelos.

    class Meta:
        # Configurações do serializer.
        model = StockMovement

        # Inclui todos os campos do modelo.
        fields = '__all__'

        # Impede que o cliente defina esses campos livremente.
        read_only_fields = ['created_at', 'created_by']

    def validate_quantity(self, value):
        # Verifica se a quantidade é válida.
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade deve ser maior que zero."
            )

        return value

    def validate_product(self, value):
        # Impede movimentações de produtos na lixeira.
        if value.is_deleted:
            raise serializers.ValidationError(
                "O produto está na lixeira."
            )

        return value

    def validate_unit_cost(self, value):
        # Impede custos unitários negativos.
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "O custo unitário não pode ser negativo."
            )

        return value
