
from rest_framework import serializers
from .models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    # criamos uma classe StockMovementSerializer que herda de
    # serializers.ModelSerializer, que é uma classe base do Django REST Framework para criar serializers baseados em modelos.

    class Meta:  # meta configurações do serializer
        model = StockMovement
        # definimos o modelo que será serializado,
        # que é o modelo StockMovement que criamos anteriormente.
        fields = '__all__'
        # definimos que todos os campos do modelo StockMovement
        # serão incluídos na serialização.
