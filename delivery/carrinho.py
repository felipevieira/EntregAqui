from models import Loja, ProdutosCarrinho, Produto
import datetime
import models

ID_CARRINHO = "ID_CARRINHO"

class Carrinho:
    def __init__(self,request, loja_id):
        id_carrinho = request.session.get(ID_CARRINHO)
        if (id_carrinho):
            try:
                carrinho = models.Carrinho.objects.get(id=id_carrinho);
            except:
                carrinho = self.new(request, loja_id)
        else:
            carrinho = self.new(request, loja_id)
            
        self.carrinho = carrinho 
  
    def new(self, request, loja_id):
        carrinho = models.Carrinho(data_criacao=datetime.datetime.now(), loja = Loja.objects.get(id=loja_id))
        carrinho.save()
        request.session[ID_CARRINHO] = carrinho.id
        print "Criado novo carrinho de id "+ str(carrinho.id)
        return carrinho
  
    def adiciona(self,produto_id, quantidade):
        try:
            item = ProdutosCarrinho.objects.get(
                        carrinho = self.carrinho, 
                        produto=Produto.objects.get(id=produto_id))
            item.quantidade = item.quantidade + quantidade;
            item.save()
        except:  
            ProdutosCarrinho(carrinho=self.carrinho,produto=Produto.objects.get(id=produto_id),quantidade=quantidade).save()
    
    def remove(self,produto_id, quantidade):
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
    
    def limpa(self):
        ProdutosCarrinho.objects.filter(carrinho=self.carrinho).delete()    
    
    def checkout(self):
        #enviar mensagem para a loja        
        pass
    
    def __str__(self):
        result = "["
        sep = ""
        for linha in ProdutosCarrinho.objects.filter(carrinho=self.carrinho):
            result += sep + str(linha.produto.nome) + " - "  + str(linha.quantidade) + " itens"
            sep= ","
        result += "]"
        result += "; "
        result += "Valor: " + str(self.total())
        return result