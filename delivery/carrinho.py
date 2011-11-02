from models import Loja, ProdutosCarrinho, Pedido, Produto
import datetime


ID_CARRINHO = "ID_CARRINHO"

class Carrinho:
#   O request dos metodos sera usado por questoes de verificacao (seguranca)
    def __init__(self, request, loja_id):
        id_carrinho = request.session.get(ID_CARRINHO)
        if (id_carrinho):
            try:
                carrinho = Pedido.objects.get(id=id_carrinho);
            except:
                carrinho = self.new(request, loja_id)
        else:
            carrinho = self.new(request, loja_id)
            
        self.carrinho = carrinho 

    def new(self, request, loja_id):
        carrinho = Pedido(data_criacao=datetime.datetime.now(),
                          loja = Loja.objects.get(id=loja_id), status = "ABERTO")
        carrinho.save()
        request.session[ID_CARRINHO] = carrinho.id
        print "Criado novo carrinho de id "+ str(carrinho.id)
        return carrinho

    def adiciona(self, request, produto_id, quantidade):
        try:
            item = ProdutosCarrinho.objects.get(
                        carrinho = self.carrinho, 
                        produto=Produto.objects.get(id=produto_id))
            item.quantidade = item.quantidade + quantidade;
            item.save()
        except:  
            ProdutosCarrinho(carrinho=self.carrinho,produto=Produto.objects.get(id=produto_id),quantidade=quantidade).save()
    
    def remove(self, request, produto_id, quantidade):
        try:
            item = ProdutosCarrinho.objects.get(
                        carrinho = self.carrinho, 
                        produto=Produto.objects.get(id=produto_id))
            item.quantidade = item.quantidade - quantidade;
            
            if(item.quantidade <=0):
                item.delete()
                
        except:  
            pass
        
    def total(self):
        total = 0
        for linha in ProdutosCarrinho.objects.filter(carrinho=self.carrinho):
            total += linha.produto.preco * linha.quantidade
        return total
    
    def limpa(self, request):
        ProdutosCarrinho.objects.filter(carrinho=self.carrinho).delete()    
    
    def realizarPedido(self, request):
        self.carrinho.status = "PEDIDO_REALIZADO"
        self.carrinho.save()
        
        self.limparSession(request)
#       enviarMensagem(self.carrinho.loja, self.carrinho.produtos.all())       
        pass

    def limparSession(self, request):
        request.session[ID_CARRINHO] = None
    
    def __str__(self):
        return str(self.carrinho)
