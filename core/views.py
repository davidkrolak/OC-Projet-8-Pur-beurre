from django.shortcuts import render, redirect, reverse
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

            if queryset.count() <= 0:
                return render(request, self.template_name)
            else:
                new_queryset = []
                for list in self.chunks(queryset, 3):
                    new_queryset.append(list)

                context_dict = {"queryset": new_queryset}
                return render(request, self.template_name, context_dict)

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
