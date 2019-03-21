from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm, \
    UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,
                                 required=False,
                                 help_text='Optionnel.',
                                 label='Prénom',
                                 widget=forms.TextInput(
                                         attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=30,
                                required=False,
                                help_text='Optionnel.',
                                label='Nom',
                                widget=forms.TextInput(
                                        attrs={'class': 'form-control'}))

    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(
                                     attrs={'class': 'form-control'}))

    password1 = forms.CharField(
            label=_("Password"),
            strip=False,
            help_text=password_validation.password_validators_help_text_html(),
            widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
            label=_("Password confirmation"),
            widget=forms.PasswordInput(attrs={'class': 'form-control'}),
            strip=False,
            help_text=_(
                    "Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'email', 'password1',
            'password2',)
        widgets = {'username': forms.TextInput(attrs={'class':
                                                          'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control'})
    )
    password = forms.CharField(
            label=_("Password"),
            strip=False,
            widget=forms.PasswordInput(attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')
