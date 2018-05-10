from django import forms
import re

from . import models


class MenuForm(forms.ModelForm):

    class Meta:
        model = models.Menu
        exclude = ('created_date',)

    def clean_items(self):
        data = self.cleaned_data.get('items')
        if len(data) <= 1:
            raise forms.ValidationError("Must select two or more items")
        return data


class ItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        exclude = ('created_date', )

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if not re.match(r'^\d{4}\r', data):
            raise forms.ValidationError(
                """Description must start with 4 digit ID number"""
                """, with the description starting on the next line""")
        return data
