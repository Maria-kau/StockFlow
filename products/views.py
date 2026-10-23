from rest_framework.filters import SearchFilter
# Importa a classe SearchFilter do Django REST Framework.

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView

# Importamos a classe ListCreateAPIView do Django REST Framework.
# Ela permite listar e criar objetos em uma única view.

from .models import Product
# Importamos o modelo Product que criamos anteriormente.

from .serializers import ProductSerializer
# Importamos o serializer ProductSerializer.

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    # Define a consulta que buscará todos os produtos cadastrados
    # no banco de dados.

    serializer_class = ProductSerializer# Define o serializer que será utilizado para validar
    # e converter os dados dos produtos.


    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['active']


class ProductDetailView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# OBSERVAÇÃO:
# ProductListCreateView é uma view baseada em classe.
# Ela herda de ListCreateAPIView do Django REST Framework.

# LEMBRETE:
# queryset define quais objetos serão consultados.
# serializer_class indica qual serializer a view utilizará.
