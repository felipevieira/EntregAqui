from django.http import HttpResponse
from django.shortcuts import render_to_response
from delivery.models import *

def home(request):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("home.html", { 'enderecos': enderecos })