from django import forms
from .models import Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'password1',
            'password2'
        ]


class ItemForm(forms.ModelForm):

    class Meta:

        model = Item

        fields = [
            'categoria',
            'nome',
            'codigo',
            'quantidade',
            'valor_unitario'
        ]

        widgets = {

            'categoria': forms.Select(
                attrs={
                    'class':'input'
                }
            ),

            'nome': forms.TextInput(
                attrs={
                    'class':'input'
                }
            ),

            'codigo': forms.TextInput(
                attrs={
                    'class':'input'
                }
            ),

            'quantidade': forms.NumberInput(
                attrs={
                    'class':'input'
                }
            ),

            'valor_unitario': forms.NumberInput(
                attrs={
                    'class':'input'
                }
            ),

        }