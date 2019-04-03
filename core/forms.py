from django import forms

class FoodRequestForm(forms.Form):
    research = forms.CharField(max_length=500)