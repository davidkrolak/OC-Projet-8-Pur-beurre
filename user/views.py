from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from .forms import SignUpForm


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



class AccountView(View):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        return HttpResponse(str(user.username))
