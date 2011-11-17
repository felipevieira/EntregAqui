# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login as authlogin, \
    logout as authlogout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UsuarioForm, DivErrorList, EnderecoForm, ReclamacaoForm, \
    ParceriaForm, InformarCidadeForm, LoginForm
from models import Usuario, Loja, Carrinho, Endereco, Categoria, \
    ProdutosCarrinho, Produto, EnderecoLoja, SolicitacaoCidade, Funcionario, Pedido, \
    ProdutosPedido, EnderecoUsuario
from pedidos_manager import PedidosManager
import datetime
import random
import sha
import utils
from urllib2 import request_host
from getpass import getuser

mensagem_email = "Obrigado por se cadastrar no PreguiçaDelivery.\n\n" \
           "Por favor, clique no link http://127.0.0.1:8000/cadastro/%s para ativar" \
           "a sua conta.\n\n" \
           "Caso não ative sua conta em 48 horas, a mesma será apagada.\n\n" \
           "Caso não consiga acessar o link, copie e cole o mesmo na barra de " \
           "endereço do seu navegador.\n\nObrigado.\n\n Equipe PreguiçaDelivery"

### Utils ###

def nome_usuario_logado(request):
    if request.user.is_authenticated():
        return request.user.first_name
    return "Visitante"

def get_usuario(request):
    if not request.user.is_authenticated():
        return None
    try:
        usuario = Usuario.objects.get(conta=request.user)
    except Usuario.DoesNotExist:
        try:
            usuario = Funcionario.objects.get(conta=request.user)
        except Funcionario.DoesNotExist:
            return None
    return usuario

def get_top_usuarios(loja):
    pedidos = Loja.objects.get(nome=loja).pedidos
    mais_compras = {}
    for pedido in pedidos:
        mais_compras[pedido.comprador] = mais_compras.get(pedido.comprador, 0) + 1
    mais_pagos = {}
    for pedido in pedidos:
        mais_pagos[pedido.comprador] = mais_pagos.get(pedido.comprador, 0) + \
        pedido.total_pago
    return mais_compras, mais_pagos

def template_data(request):
    dados = {}
    dados['categorias'] = Categoria.objects.all().order_by('nome')
    dados['usuario'] = get_usuario(request)
    dados['cidade'] = request.session['cidade']
    dados['lojas_categoria'] = {}
    for loja in Loja.objects.filter(endereco__cidade=request.session['cidade']):
        dados['lojas_categoria'][loja.categoria] = \
        dados['lojas_categoria'].get(loja.categoria, []) + [loja]
    return dados
    
def redireciona_usuario(request):
    try:
        cidade = request.session['cidade']
    except:
        return HttpResponseRedirect("/")
    try:
        categoria = request.session['categoria']
    except:
        return visualizar_categorias(request, cidade)
    try:
        loja = request.session['loja'].nome_curto
    except:
        return listar_lojas(request, cidade, categoria)
    return detalhar_catalogo_produtos(request, cidade, categoria, loja)
 
### Callbacks ###

def home(request):
    request.session['cidade'] = "Campina Grande"
    if request.user.is_authenticated():
        home = "home_logado.html"
    else:
        home = "home.html"
    enderecos = Endereco.objects.values('cidade').annotate()
    dados = template_data(request)
    dados['enderecos'] = enderecos
    return render_to_response(home, dados,
                              context_instance=RequestContext(request)
                )

def home_redirect(request):
    return HttpResponseRedirect("/")

def visualizar_categorias(request, cidade):
    enderecos = Endereco.objects.values('cidade').annotate()
    request.session['cidade'] = cidade
    dados = template_data(request)
    return render_to_response("categorias.html", dados,
                              context_instance=RequestContext(request))

def listar_lojas(request, cidade, categoria):
    request.session['cidade'] = cidade
    request.session['categoria'] = categoria
    enderecos = Endereco.objects.values('cidade').annotate()
    lojas = Loja.objects.filter(endereco__cidade=cidade, categoria__nome=categoria)
    dados = template_data(request)
    dados['categoria'] = categoria
    dados['cidade'] = cidade
    dados['lojas'] = lojas
    return render_to_response("lojas.html", dados,
                              context_instance=RequestContext(request))

def iniciar_pagamento(request, cidade, categoria, loja):
    nome_loja = request.session['loja']
    cidade = request.session['cidade']
    
    loja = Loja.objects.get(nome_curto=loja,
                                               endereco__cidade=cidade)
    
    dados = template_data(request)    
    
    carrinho = Carrinho.objects.get(loja=nome_loja,comprador=get_usuario(request))
    
    total_a_pagar = 0
    
    for produto in carrinho.produtos.all():
        total_a_pagar += produto.preco
        
    
    dados['carrinho'] = carrinho
    dados['loja'] = loja
    dados['total'] = total_a_pagar
    
    
    return render_to_response("pagamento.html", dados)

def exibir_painel_fale_conosco(request):
    return render_to_response("fale_conosco.html", context_instance=RequestContext(request))

def exibir_obrigado_fale_conosco(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        assunto = request.POST['assunto']
        telefone = request.POST['telefone']
        texto = request.POST['texto']
        utils.enviar_contato(nome, email, assunto, telefone, texto)
    return render_to_response("obrigado_fale_conosco.html", context_instance=RequestContext(request))

def detalhar_catalogo_produtos(request, cidade, categoria, loja):
    request.session['cidade'] = cidade
    request.session['categoria'] = categoria
    request.session['loja'] = Loja.objects.get(nome_curto=loja,
                                               endereco__cidade=cidade)
    dados = template_data(request)
    if request.method == 'POST':
        usuario = get_usuario(request)
        if not usuario:
            return HttpResponseRedirect("/")
        comprou = False
        produtos = []
        for produto, quantidade in request.POST.items():
            try:
                if int(quantidade) == 0:
                    continue
            except ValueError:
                continue
            if not comprou:
                comprou = True
                carrinho, criado = Carrinho.objects.\
                get_or_create(loja=Loja.objects.get(endereco__cidade=cidade,
                                                    nome_curto=loja),
                              comprador=usuario,
                              total_pago=0)
                
            if produto.startswith("quantidade"):
                produto_id = int(produto.split("_")[1])
                
                try:
                    produto_desejado = ProdutosCarrinho.objects.get(carrinho=carrinho,
                                                   produto=Produto.objects.get(id=produto_id))                    
                    quantidade_antiga = produto_desejado.quantidade
                    quantidade_nova = int(quantidade) + int(quantidade_antiga)                    
                    ProdutosCarrinho.objects.filter(carrinho=carrinho,produto=Produto.objects.get(id=produto_id)).update(quantidade = quantidade_nova )
                
                except ProdutosCarrinho.DoesNotExist:
                    produto_carrinho = ProdutosCarrinho(carrinho=carrinho,
                                                   produto=Produto.objects.get(id=produto_id),
                                                   quantidade=int(quantidade))
                    produto_carrinho.save()
                    produtos.append(produto_carrinho)                    
                    
                 
                
        if not comprou:
            return HttpResponseRedirect("")
        total_pago = 0
        for produto in ProdutosCarrinho.objects.filter(carrinho=carrinho):
            for i in range(produto.quantidade):
                total_pago += produto.produto.preco
        carrinho.total_pago = total_pago
        #carrinho.save()
        dados['carrinho'] = carrinho
        dados['produtos'] = produtos
        
    enderecos = EnderecoLoja.objects.values('cidade').annotate()
    produtos = Produto.objects.filter(catalogo__loja__nome_curto=loja,
                                      catalogo__loja__endereco__cidade=cidade,
                                      catalogo__loja__categoria__nome=categoria)
    dados['produtos'] = produtos
    dados['loja'] = loja
    dados['categoria'] = categoria
    return render_to_response("catalogo.html", dados,
                              context_instance=RequestContext(request))

def cadastrar_usuario(request):
    dados = template_data(request)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, auto_id=False, error_class=DivErrorList)
        if form.is_valid():
            u = form.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            chave = sha.new(salt + u.username).hexdigest()
            expira = datetime.datetime.today() + datetime.timedelta(2)
            usuario = Usuario(conta=u,
                             cpf=form.cleaned_data['cpf'],
                             chave_de_ativacao=chave,
                             expiracao_chave=expira,
                             nascimento=form.cleaned_data['nascimento'],
                             sexo=form.cleaned_data['sexo'])
            request.session['pass'] = form.cleaned_data['senha']
            request.session['conta'] = u
            request.session['usuario_cadastro'] = usuario
            form = EnderecoForm()
            dados['form'] = form
            return render_to_response('finalizar_cadastro.html', dados,
                              context_instance=RequestContext(request))
        else:
            dados['form'] = form
            return render_to_response('cadastro.html', dados,
                                      context_instance=RequestContext(request))
    else:
        form = UsuarioForm()
        dados['form'] = form
    return render_to_response('cadastro.html', dados,
                              context_instance=RequestContext(request))

def finalizar_cadastro(request):
    try:
        conta = request.session['conta']
        usuario = request.session['usuario_cadastro']
    except KeyError:
        return HttpResponseRedirect("/cadastro/")
    dados = template_data(request)
    if request.method == 'POST':
        form = EnderecoForm(request.POST, auto_id=False, error_class=DivErrorList)
        if form.is_valid():
            conta.save()
            usuario.save()
            endereco = EnderecoUsuario(logradouro=form.cleaned_data['logradouro'],
                                       numero=form.cleaned_data['numero'],
                                       complemento=form.cleaned_data['complemento'],
                                       bairro=form.cleaned_data['bairro'],
                                       cep=form.cleaned_data['cep'],
                                       cidade=form.cleaned_data['cidade'],
                                       estado=form.cleaned_data['estado'],
                                       referencia=form.cleaned_data['referencia'],
                                       usuario=usuario)
            endereco.save()
#            from django.core.mail import EmailMessage
#            email = EmailMessage("Obrigado por se cadastrar no Preguiça Delivery",
#                                 mensagem_email % usuario.chave_de_ativacao,
#                                 to=[usuario.conta.email])
#            email.send()
            del request.session['conta']
            del request.session['usuario_cadastro']
            conta_logada = authenticate(username=conta.username,
                                        password=request.session['pass'])
            authlogin(request, conta_logada)
            del request.session['pass']
            return painel(request)
        else:
            dados['form'] = form
            return render_to_response('finalizar_cadastro.html', dados,
                              context_instance=RequestContext(request))
    else:
        form = EnderecoForm()
        dados['form'] = form
    return render_to_response('finalizar_cadastro.html', dados, context_instance=RequestContext(request))

def ativar_usuario(request, chave):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    try:
        usuario = Usuario.objects.get(chave_de_ativacao=chave)
    except Usuario.DoesNotExist:
        return HttpResponseRedirect("/")
    if usuario.conta.is_active:
        return HttpResponseRedirect("/")
    if usuario.expiracao_chave < datetime.datetime.today():
        return HttpResponse("expirou!")
    conta = usuario.conta
    conta.is_active = True
    conta.save()
    usuario.chave_de_ativacao = ""
    usuario.save()
    conta = authenticate(username=conta.username,
                         password=conta.password)
    authlogin(request, conta)
    return HttpResponseRedirect("/adicionar_endereco")

def exibir_pedidos(request):
    return render_to_response("ultimos_pedidos.html",
                              {'usuario' : request.user})
    
def exibir_parceria(request):
    if request.method == 'POST':
        form = ParceriaForm(request.POST)
        if form.is_valid():   
            utils.enviar_pedido_parceria(utils.getConteudoEmailPedido(form.cleaned_data['empresa'], form.cleaned_data['email'],
                                                                       form.cleaned_data['contato']), form.cleaned_data['empresa'])
            return HttpResponse('Pedido enviado com sucesso.');
    else:
        form = ParceriaForm()
        
    return render_to_response("parceria.html",
                              {'form': form}, context_instance=RequestContext(request))
    
def exibir_disponibilidade(request):
    if request.method == 'POST':
        form = InformarCidadeForm((request.POST))
        if form.is_valid():        
            solicitacao = SolicitacaoCidade()
            solicitacao.nomeUsuario = form.cleaned_data['nome']
            solicitacao.emailUsuario = form.cleaned_data['email']
            solicitacao.cidade = form.cleaned_data['cidade']
            solicitacao.save()
            return HttpResponse('Solicitacao realizada com sucesso.');
    else:
        form = InformarCidadeForm()
        
    return render_to_response("disponibilidade_cidade.html",
                              {'form': form}, context_instance=RequestContext(request))
    
def exibir_menu_usuario(request):
    return render_to_response("menu_usuario.html")
    
def adicionar_endereco(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = Endereco(logradouro=form.cleaned_data['logradouro'],
                                numero=form.cleaned_data['numero'],
                                complement=form.cleaned_data['complemento'],
                                bairro=form.cleaned_data['bairro'],
                                cep=form.cleaned_data['cep'],
                                cidade=form.cleaned_data['cidade'],
                                estado=form.cleaned_data['estado'],
                                referencia=form.cleaned_data['referencia'],
                                usuario=request.user)
            endereco.save()
            return HttpResponse("Endereco adicionado com sucesso!")
    return render_to_response("adicionar_endereco.html",
                              {'form' : EnderecoForm()},
                              context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            conta = authenticate(username=form.cleaned_data['login'],
                                 password=form.cleaned_data['senha'])     
            authlogin(request, conta)
            return redireciona_usuario(request)
        else:
            return render_to_response("login_erro.html",
                              {'form' : form},
                              context_instance=RequestContext(request))
            
    else:
        form = LoginForm()
    return render_to_response("login.html",
                              {'form' : form},
                              context_instance=RequestContext(request))

def logout(request):
    authlogout(request)
    return HttpResponseRedirect("/")

def painel(request):
    usuario = get_usuario(request)
    if usuario is None:
        return HttpResponseRedirect("/")
    if isinstance(usuario, Usuario):
        dados = template_data(request)
        dados['endereco'] = EnderecoUsuario.objects.get(usuario=usuario)
        return render_to_response("painel_usuario_cadastro.html", dados,
                                  context_instance=RequestContext(request)
                                  )
    if isinstance(usuario, Funcionario):
        mais_compras, mais_pagos = get_top_usuarios(request.user.usuario.loja)
        return render_to_response("painel_cliente.html",
                                  {'usuario': request.user,
                                   'mais_compras': mais_compras,
                                   'mais_pagos': mais_pagos},
                                  context_instance=RequestContext(request)
                                  )
    return HttpResponseRedirect("/")

def finaliza_compra(request):
    usuario = get_usuario(request)
    if usuario is None:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        try:
            carrinho = Carrinho.objects.get(comprador=usuario)
        except Carrinho.DoesNotExist:
            return redireciona_usuario(request)
        pedido = Pedido(comprador=usuario,
                        loja=request.session['loja'],
                        data_criacao=datetime.datetime.now(),
                        status="ABERTO",
                        total_pago=carrinho.total_pago)
        pedido.save()
        for produto_carrinho in carrinho.produtos_carrinho.all():
            produto = ProdutosPedido(pedido=pedido,
                                     produto=produto_carrinho.produto,
                                     quantidade=produto_carrinho.quantidade)
            produto.save()
        return render_to_response("painel_usuario.html",
                                  {'usuario' : request.user,
                                   'comprou' : True},
                                  context_instance=RequestContext(request))
    return redireciona_usuario(request)


def exibir_catalogo(request):
    return render_to_response("catalogo.html")

def exibir_confirmacao_adicao(request):
    return render_to_response("confirma_adicao_carrinho.html")
    
def exibir_ajuda(request):
    return render_to_response("entenda_preguica.html")

def exibir_carrinho(request):
    nome_loja = request.session['loja']
    cidade = request.session['cidade']
    
    dados = template_data(request)    
    
    carrinho = Carrinho.objects.get(loja=nome_loja,comprador=get_usuario(request))
    
    dados['carrinho'] = carrinho
    return render_to_response("confirma_compra.html",
                                  dados,
                                  context_instance=RequestContext(request))
