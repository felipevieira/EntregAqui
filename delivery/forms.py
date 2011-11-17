# -*- coding: utf-8 -*-

from delivery.models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRZipCodeField, BRCPFField,\
    BRPhoneNumberField
from django.forms.models import ModelForm
from models import Usuario, Endereco, CustomUsuario
from models import *
from datetime import *
from django.forms.widgets import Media
from django.forms.util import ErrorList

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: 
            return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


class UsuarioForm(forms.Form):
    sexo_choices = (("M", "Masculino"), ("F", "Feminino"))
    username = forms.CharField(max_length=30, label=u'Login desejado', error_messages={'required':'Por favor, digite o username desejado'})
    nome = forms.CharField(max_length=20, label=u"Nome")
    sobrenome = forms.CharField(max_length=50, label=u"Sobrenome")
    cpf = BRCPFField(label=u"CPF")
    sexo = forms.ChoiceField(label=u"Sexo", choices=sexo_choices)
    nascimento = forms.DateField(label=u'Data de Nascimento', input_formats=['%d/%m/%Y'])
    telefone_contato = BRPhoneNumberField(label=u"Telefone para Contato (XX-XXXX-XXXX)", error_messages={'invalid':'O telefone deve estar no formato XX-XXXX-XXXX'})
    email = forms.EmailField(label=u'Email')
    repetir_email = forms.EmailField(label=u'Repetir Email')    
    senha = forms.CharField(min_length=6,
                            label=u'Senha',
                            widget=forms.PasswordInput(render_value=False))
    repetir_senha = forms.CharField(min_length=6,
                                    label=u'Repetir senha',
                                    widget=forms.PasswordInput(render_value=False))
    
    def clean_repetir_email(self):
        if (self.cleaned_data['email'] != self.cleaned_data['repetir_email']):
            raise forms.ValidationError(u'Emails não estão iguais.')
        else:
            try:
                CustomUsuario.objects.get(conta__email=self.cleaned_data['email'])
            except CustomUsuario.DoesNotExist:
                return self.cleaned_data['repetir_email']
            raise forms.ValidationError(u'Email já cadastrado no sistema!')
    
    def clean_repetir_senha(self):
        if (self.cleaned_data['senha'] != self.cleaned_data['repetir_senha']):
            raise forms.ValidationError(u'Senhas não estão iguais.')
        else:
            return self.cleaned_data['repetir_senha']
        
    def clean_username(self):
        try:
            conta = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        if not conta.is_active:
            conta.delete()
            return self.cleaned_data['username']
        raise forms.ValidationError(u'Login já existe!')
    
    def clean_cpf(self):
        try:
            User.objects.get(username=self.cleaned_data['cpf'])
        except User.DoesNotExist:
            return self.cleaned_data['cpf']
        raise forms.ValidationError(u'CPF ja cadastrado!')
    
    def save(self):
        usuario = User.objects.create_user(self.cleaned_data['username'],
                                           self.cleaned_data['email'],
                                           self.cleaned_data['senha'])
        usuario.first_name = self.cleaned_data['nome']
        usuario.last_name = self.cleaned_data['sobrenome']
        usuario.is_active = False
        usuario.save()
        return usuario
    
    class Media:
        css = { 'all' : '/static/style/styleForms.css'
        }

class EnderecoForm(ModelForm):
    cep = BRZipCodeField(label=u'CEP')
    
    class Meta:
        model = EnderecoUsuario
        exclude = ('usuario',)
    
    class Media:
        css = { 'all' : '/static/style/styleForms.css'
        }
        
class ReclamacaoForm(forms.Form):
    reclamacao = forms.CharField(widget=forms.Textarea(),
                                 initial="Digite sua reclamação aqui.",
                                 label="")

class LoginForm(forms.Form):
    login = forms.CharField(min_length=6, label=u'Login')
    senha = forms.CharField(min_length=6,
                            label=u'Senha',
                            widget=forms.PasswordInput(render_value=False))
    
    def clean_senha(self):
        try:
            usuario = CustomUsuario.objects.get(conta__username=
                                                self.cleaned_data['login'])
        except CustomUsuario.DoesNotExist:
            raise forms.ValidationError(u'Login ou senha inválidos!')
        if not usuario.conta.check_password(self.cleaned_data['senha']):
            raise forms.ValidationError(u'Login ou senha inválidos!')
        return self.cleaned_data['senha']
    
class ParceriaForm(forms.Form):
    empresa = forms.CharField(max_length=100, label=u"Nome da Empresa")
    email = forms.EmailField(label=u"Email")
    contato = forms.CharField(max_length=10, label=u"Telefone para Contato")
    
class InformarCidadeForm(forms.Form):
    nome = forms.CharField(max_length=50, label=u"Nome")
    email = forms.EmailField(label=u"Email")
    cidade = forms.CharField(max_length=50, label=u"Cidade")
