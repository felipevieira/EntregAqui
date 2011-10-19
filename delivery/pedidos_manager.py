from models import Carrinho, Loja


class PedidosManager:
    
    def ultimos_pedidos(self, loja_id):
        return Carrinho.objects.filter(loja = Loja.objects.filter(id=loja_id), status = 'PEDIDO_REALIZADO')