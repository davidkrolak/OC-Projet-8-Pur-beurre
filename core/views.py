from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .models import Food
from .forms import FoodRequestForm


class HomeView(View):
    form = FoodRequestForm
    template_name = 'core/home.html'

    def get(self, request):
        form = self.form
        context_dict = {'form': form}
        return render(request, self.template_name, context_dict)


class ResearchView(View):
    form = FoodRequestForm
    template_name = 'core/research.html'

    def get(self, request):
        form = self.form(request.GET)
        if form.is_valid():
            research = form.cleaned_data.get('food')
            queryset = Food.objects.filter(name__icontains=research)
            if queryset.count() == 0:
                return redirect('core:no_result')
            else:
                context_dict = {"queryset": queryset}
                return render(request, self.template_name, context_dict)
