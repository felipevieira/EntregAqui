# -*- coding: utf-8 -*-

from delivery.models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRZipCodeField, BRCPFField
from django.forms.models import ModelForm
from models import Usuario, Endereco, CustomUsuario
from django.contrib.auth import authenticate

class UsuarioForm(forms.Form):
    username = forms.CharField(max_length=30, label=u'Login')
    nome = forms.CharField(max_length=20)
    sobrenome = forms.CharField(max_length=50)
    email = forms.EmailField(label=u'Email')
    repetir_email = forms.EmailField(label=u'Repetir Email')
    cpf = BRCPFField(label=u"CPF")
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
            return forms.ValidationError(u'Email já cadastrado no sistema!')
    
    def clean_repetir_senha(self):
        if (self.cleaned_data['senha'] != self.cleaned_data['repetir_senha']):
            raise forms.ValidationError(u'Senhas não estão iguais.')
        else:
            return self.cleaned_data['repetir_senha']
        
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(u'Login já existe!')
    
    def save(self):
        usuario = User.objects.create_user(self.cleaned_data['username'],
                                           self.cleaned_data['email'],
                                           self.cleaned_data['senha'])
        usuario.first_name = self.cleaned_data['nome']
        usuario.last_name = self.cleaned_data['sobrenome']
        usuario.is_active = False
        usuario.save()
        return usuario

class EnderecoForm(ModelForm):
    cep = BRZipCodeField(label=u'CEP')
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(),
                                     widget=forms.HiddenInput())
    
    class Meta:
        model = Endereco
        
class ReclamacaoForm(forms.Form):
    reclamacao = forms.CharField(widget=forms.Textarea(),
                                 initial="Digite sua reclamação aqui.",
                                 label="")

class LoginForm(forms.Form):
    login = forms.CharField(min_length=6, label=u'Login')
    senha = forms.CharField(min_length=6,
                            label=u'Senha',
                            widget=forms.PasswordInput(render_value=False))
    
    def clean_login(self):
        try:
            usuario = CustomUsuario.objects.get(conta__username=
                                                self.cleaned_data['login'])
        except CustomUsuario.DoesNotExist:
            raise forms.ValidationError(u'Login ou senha inválidos!')
        return self.cleaned_data['login']
    
    def clean_senha(self):
        try:
            usuario = CustomUsuario.objects.get(conta__username=
                                                self.cleaned_data['login'])
        except CustomUsuario.DoesNotExist:
            raise forms.ValidationError(u'Login ou senha inválidos!')
        if not usuario.conta.check_password(self.cleaned_data['senha']):
            raise forms.ValidationError(u'Login ou senha inválidos!')
        return self.cleaned_data['senha']