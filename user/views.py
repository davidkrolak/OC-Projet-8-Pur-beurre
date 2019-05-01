from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SignUpForm, LoginForm


class SignUpView(View):
    form = SignUpForm
    template_name = 'user/signup.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user:account')
        elif not form.is_valid():
            form = self.form()
            return render(request, self.template_name, {'form': form})


class ConnectionView(LoginView):
    template_name = 'user/login.html'
    authentication_form = LoginForm


class DisconnectionView(LogoutView):

    def get(self, request, *args, **kwargs):
        return redirect('core:home')


class AccountView(View):
    template_name = 'user/account.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        context_dict = {'user': user}
        return render(request, self.template_name, context_dict)
