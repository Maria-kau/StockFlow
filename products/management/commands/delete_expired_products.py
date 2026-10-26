# Importa timedelta para calcular um intervalo de tempo de 30 dias.
from datetime import timedelta

# Importa a classe necessária para criar comandos personalizados do Django.
from django.core.management.base import BaseCommand

# Importa a exceção lançada quando uma exclusão é bloqueada
# por um relacionamento protegido no banco de dados.
from django.db.models import ProtectedError

# Importa ferramentas para trabalhar com data e hora.
from django.utils import timezone

# Importa o modelo Product, que representa os produtos do StockFlow.
from products.models import Product


class Command(BaseCommand):
    # Descrição do comando, exibida na ajuda do Django.
    help = "Excluir produtos da lixeira após 30 dias!"

    def handle(self, *args, **options):
        # Calcula a data-limite: data e hora atuais menos 30 dias.
        # Produtos excluídos antes ou nessa data podem ser removidos.
        limite = timezone.now() - timedelta(days=30)

        # Busca somente os produtos que estão na lixeira
        # e cuja data de exclusão atingiu o prazo de 30 dias.
        produtos = Product.objects.filter(
            is_deleted=True,
            deleted_at__lte=limite
        )

        # Contador de produtos excluídos definitivamente com sucesso.
        excluidos = 0

        # Contador de produtos preservados por terem movimentações
        # de estoque que impedem sua exclusão.
        preservados = 0

        # Percorre os produtos encontrados na consulta.
        # iterator() permite percorrer os resultados sem carregar
        # toda a coleção de objetos de uma só vez na memória.
        for produto in produtos.iterator():
            try:
                # Tenta excluir definitivamente o produto do banco de dados.
                produto.delete()

                # Se a exclusão funcionar, incrementa o contador.
                excluidos += 1

            except ProtectedError:
                # Se houver uma relação protegida, preserva o produto
                # e mantém seu histórico de movimentações.
                preservados += 1

        # Exibe a quantidade de produtos excluídos com uma mensagem
        # formatada pelo Django como mensagem de sucesso.
        self.stdout.write(
            self.style.SUCCESS(
                f"Produtos excluídos: {excluidos}"
            )
        )

        # Exibe a quantidade de produtos que não puderam ser excluídos
        # devido à proteção das movimentações de estoque.
        self.stdout.write(
            f"Produtos preservados por terem movimentações: {preservados}"
        )