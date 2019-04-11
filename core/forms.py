from django import forms
from .models import Categories


class FoodRequestForm(forms.Form):
    food = forms.CharField(max_length=500,
                           widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Produit',
                                          'aria-label': 'Produit'}
                           ))


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('name', 'product_count', 'url', 'off_id')
