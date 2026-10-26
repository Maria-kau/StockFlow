from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone

from rest_framework.filters import SearchFilter
# Importa a classe SearchFilter do Django REST Framework.

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
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


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().filter(is_deleted=False)
    serializer_class = ProductSerializer

    def perform_destroy(self,destroy):
        # marca a data e a hora do produto foi excluido
        destroy.deleted_at = timezone.now()
        # envia o produto pra lixeira sem excluir
        destroy.is_deleted = True

        destroy.save(update_fields=['is_deleted', 'deleted_at'])

class ProductTrashListView(ListAPIView):
    queryset = Product.objects.filter(is_deleted=True).order_by('id')
    serializer_class = ProductSerializer

class ProductRestoreView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self,request,pk):
        product = get_object_or_404(Product, id=pk, is_deleted=True)

        product.is_deleted = False #salva
        product.deleted_at = None#salva

        product.save(update_fields=['is_deleted','deleted_at'])

        #devolver a resposta para o serialize

        serializer = ProductSerializer (product)
        return Response(
            serializer.data , status=status.HTTP_200_OK
        )



# OBSERVAÇÃO:
#O get_object_or_404 é uma função de atalho do Django 
# que tenta buscar um registro no banco de dados.


#pk=significa primeira chave ou seja id
# ProductListCreateView é uma view baseada em classe.
# Ela herda de ListCreateAPIView do Django REST Framework.

# LEMBRETE:
# queryset define quais objetos serão consultados.
# serializer_class indica qual serializer a view utilizará.
