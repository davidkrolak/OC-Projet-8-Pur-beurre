from django import forms
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm, \
    UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,
                                 required=False,
                                 help_text='Optionnel.',
                                 label='Prénom')
    last_name = forms.CharField(max_length=30,
                                required=False,
                                help_text='Optionnel.',
                                label='Nom')
    email = forms.EmailField(max_length=254, )

    class Meta():
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'email', 'password1',
            'password2',)


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs=
                                                    {'autofocus': True,
                                                     'class': 'form-control'}))
    password = forms.CharField(
            label=_("Password"),
            strip=False,
            widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta():
        model = User
        fields = ('username', 'password')
