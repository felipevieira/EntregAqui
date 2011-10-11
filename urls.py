from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'delivery.views.home', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cadastro/?P<chave>[\w]+', 'EntregAqui.delivery.views.ativar_usuario'),
    url(r'^cadastro/', 'EntregAqui.delivery.views.cadastrar_usuario'),
    url(r'^painel/', 'EntregAqui.delivery.views.visualizar_painel_usuario'),
    url(r'^reclamar/', 'EntregAqui.delivery.views.exibir_reclamacao'),
    #[\w ]+ para pegar espaco
    (r'^(?P<cidade>[\w ]+)/(?P<categoria>[\w ]+)/(?P<loja>[\w ]+)/$', 'EntregAqui.delivery.views.detalhar_catalogo_produtos'),
    (r'^(?P<cidade>[\w ]+)/(?P<categoria>[\w ]+)/$', 'EntregAqui.delivery.views.listar_lojas'),
    (r'^(?P<cidade>[\w ]+)/$', 'EntregAqui.delivery.views.visualizar_categorias'),
    
)
