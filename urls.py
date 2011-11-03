from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'delivery.views.home', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    url(r'^cadastro/(?P<chave>[\w]+)', 'EntregAqui.delivery.views.ativar_usuario'),
    url(r'^cadastro/', 'EntregAqui.delivery.views.cadastrar_usuario'),
    url(r'^adicionar_endereco', 'EntregAqui.delivery.views.adicionar_endereco'),
    url(r'^painel/', 'EntregAqui.delivery.views.painel'),
    url(r'^fale_conosco/', 'EntregAqui.delivery.views.exibir_painel_fale_conosco'),
    url(r'^obrigado_fale_conosco/', 'EntregAqui.delivery.views.exibir_obrigado_fale_conosco'),
    url(r'^login/', 'EntregAqui.delivery.views.login'),
    url(r'^logout/', 'EntregAqui.delivery.views.logout'),
    url(r'^parceria/', 'EntregAqui.delivery.views.exibir_parceria'),
    url(r'^disponibilidade_cidade/', 'EntregAqui.delivery.views.exibir_disponibilidade'),
    url(r'^ultimos_pedidos/', 'EntregAqui.delivery.views.exibir_pedidos'),
    url(r'^menu_usuario/', 'EntregAqui.delivery.views.exibir_menu_usuario'),
    #[\w ]+ para pegar espaco
    (r'^(?P<cidade>[\w ]+)/(?P<categoria>[\w ]+)/(?P<loja>[\w ]+)/$', 'EntregAqui.delivery.views.detalhar_catalogo_produtos'),
    (r'^(?P<cidade>[\w ]+)/(?P<categoria>[\w ]+)/$', 'EntregAqui.delivery.views.listar_lojas'),
    (r'^(?P<cidade>[\w ]+)/$', 'EntregAqui.delivery.views.visualizar_categorias'),
    
)
