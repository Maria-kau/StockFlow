from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    # nome do produto com no máximo 100 caracteres
    description = models.TextField(blank=True)
    # permite que a descrição do produto seja opcional
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # preço do produto com até 10 dígitos e 2 casas decimais
    stock = models.PositiveIntegerField(default=0)
    # quantidade de produtos em estoque
    active = models.BooleanField(default=True)
    # indica se o produto está ativo ou inativo
    is_deleted = models.BooleanField(default=False)
    #is_deleted identifica se o produto foi enviado
    # para a lixeira. Todo produto novo começa com False
    deleted_at = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # cria automaticamente a data e hora de criação do produto
    updated_at = models.DateTimeField(auto_now=True)
    # atualiza automaticamente a data

    def __str__(self):
        return self.name
