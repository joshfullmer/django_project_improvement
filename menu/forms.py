from django import forms

from . import models


class MenuForm(forms.ModelForm):

    class Meta:
        model = models.Menu
        exclude = ('created_date',)


class ItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        exclude = ('created_date', )
