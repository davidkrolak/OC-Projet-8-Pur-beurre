from django.shortcuts import render
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


class SubstituteView(View):
    template_name = 'core/substitute.html'

    def get(self, request, id):
        food = Food.objects.get(id=id)
        categories = food.categories.all().order_by('id')
        nutriscore_list = self.nutriscore_list(food.nutriscore)

        queryset = Food.objects.filter(categories=categories[0]).filter(
                nutriscore__in=nutriscore_list).exclude(id=id)

        for category in categories[1:5]:
            query = Food.objects.filter(categories=category).filter(
                    nutriscore__in=nutriscore_list).exclude(id=id)
            queryset = queryset.intersection(query)

        if queryset.count() == 0:
            return render(request, self.template_name)
        else:
            new_queryset = []
            for list in self.chunks(queryset, 3):
                new_queryset.append(list)

            context_dict = {"queryset": new_queryset}
            return render(request, self.template_name, context_dict)

    def nutriscore_list(self, nutriscore):
        if nutriscore == 'A':
            return ['A']
        elif nutriscore == 'B':
            return ['A']
        elif nutriscore == 'C':
            return ['A', 'B']
        elif nutriscore == 'D':
            return ['A', 'B', 'C']
        elif nutriscore == 'E':
            return ['A', 'B', 'C', 'D']
        elif nutriscore == 'Z':
            return ['A', 'B', 'C', 'D', 'E']

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class ProductView(View):
    template_name = 'core/product.html'

    def get(self, request, id):
        food = Food.objects.get(id=id)

        context_dict = {'food': food}

        return render(request, self.template_name, context_dict)
