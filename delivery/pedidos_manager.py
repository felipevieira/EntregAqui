from models import Pedido, Loja


class PedidosManager:
    
    def ultimos_pedidos(self, loja_id):
        return Pedido.objects.filter(loja = Loja.objects.filter(id=loja_id), status = 'PEDIDO_REALIZADO')