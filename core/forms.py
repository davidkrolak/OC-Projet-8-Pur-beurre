from django import forms


class FoodRequestForm(forms.Form):
    food = forms.CharField(max_length=500,
                               widget=forms.TextInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Produit',
                                              'aria-label': 'Produit'}
                               ))
