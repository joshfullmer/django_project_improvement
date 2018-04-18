from django import forms

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)
