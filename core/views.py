from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .models import Food
from .forms import FoodRequestForm


class HomeView(View):
    form = FoodRequestForm
    template_name = "core/home.html"

    def get(self, request):
        form = self.form
        context_dict = {'form': form}
        return render(request, self.template_name, context_dict)


class ResearchView(View):
    form = FoodRequestForm
    template_name = "core/research.html"

    def get(self, request):
        form = self.form(request.GET)
        page = request.GET.get('page')
        if form.is_valid():
            research = form.cleaned_data.get('food')
            queryset = Food.objects.filter(name__icontains=research)

            if queryset.count() <= 0:
                return render(request, self.template_name)
            else:
                new_queryset = []
                for list in self.chunks(queryset, 3):
                    new_queryset.append(list)

                paginator = Paginator(new_queryset, 10)
                foods = paginator.get_page(page)
                context_dict = {"queryset": foods}
                return render(request, self.template_name, context_dict)

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class SubstituteView(View):
    template_name = 'core/substitute.html'

    def get(self, request, id):
        page = request.GET.get('page')
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

            paginator = Paginator(new_queryset, 10)
            foods = paginator.get_page(page)
            context_dict = {"queryset": foods,
                            "research": food}
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


class FavoriteFoodView(View):
    """"""
    template_name = 'core/favorite.html'

    @method_decorator(login_required)
    def post(self, request):
        food_id = request.POST['food_id']
        user = request.user
        if user.profile.favorite_foods.filter(id=food_id).count() == 1:
            return JsonResponse({})
        elif user.profile.favorite_foods.filter(id=food_id).count() == 0:
            user.profile.favorite_foods.add(food_id)
            return JsonResponse({'status': 'ok'})

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        page = request.GET.get('page')
        food = user.profile.favorite_foods.all()
        return render(request, self.template_name)

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class LegalNoticeView(View):
    template_name = 'core/legal_notice.html'

    def get(self, request):
        return render(request, self.template_name)
