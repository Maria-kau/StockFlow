
# Importa as ferramentas de serialização e validação do Django REST Framework.
from rest_framework import serializers

# Importa o modelo Product do arquivo models.py.
from .models import Product


# Cria um serializer baseado no modelo Product.
# Ele converte os dados do produto para formatos como JSON
# e valida os dados recebidos pela API.
class ProductSerializer(serializers.ModelSerializer):

    # Define as configurações do serializer.
    class Meta:
        # Indica qual modelo será utilizado.
        model = Product

        # Inclui todos os campos do modelo na serialização.
        fields = '__all__'

        read_only_fields = [
            'id',#identificador gerenciado pelo banco
            'created_at',#marca a data criada
            'updated_at',# marca a data que atualizada
            'is_deleted', #controlado pela exclução logica
            'deleted_at'#controlado pela exclução logica
        ]

    # Valida o preço recebido antes de salvar o produto.
    def validate_price(self, value):
        # Verifica se o preço é negativo.
        if value < 0:
            # Interrompe a validação e retorna uma mensagem de erro.
            raise serializers.ValidationError(
                "O preço não pode ser negativo."
            )

        # Retorna o preço quando ele passa pela validação.
        return value

    # Valida a quantidade de estoque recebida.
    def validate_stock(self, value):
        # Impede que o estoque tenha uma quantidade negativa.
        # O valor zero é permitido.
        if value < 0:
            # Retorna um erro de validação para a API.
            raise serializers.ValidationError(
                "O estoque não pode ser negativo."
            )

        # Retorna a quantidade quando ela é válida.
        return value

    # Valida o nome do produto recebido.
    def validate_name(self, value):
        # Remove espaços em branco do início e do fim do nome.
        value = value.strip()

        # Verifica se o nome ficou vazio após remover os espaços.
        if not value:
            # Impede o cadastro e retorna uma mensagem de erro.
            raise serializers.ValidationError(
                "O nome do produto não pode estar vazio."
            )

        # Retorna o nome já tratado.
        return value
