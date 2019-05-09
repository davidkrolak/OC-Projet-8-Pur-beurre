from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .models import Food
from .forms import FoodRequestForm


class HomeView(View):
    """Return the home template to the user and pass the
    food request form for the research bar in the template"""
    form = FoodRequestForm
    template_name = "core/home.html"

    def get(self, request):
        form = self.form
        context_dict = {'form': form}
        return render(request, self.template_name, context_dict)


class ResearchView(View):
    """Return results from a food research in the db with a 2d list format,
    or no context dict if there is no results"""
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
                if request.user.is_authenticated:
                    foods = request.user.profile.favorite_foods.all()
                    context_dict['favorite_foods'] = foods

                return render(request, self.template_name, context_dict)

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class SubstituteView(View):
    """Return a 2d list filled with food substitute by doing a db research
    where all the element with a lower nutrition grade are filtered and all
    the elements who doesn't share 5 categories or more with our research"""
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
            if request.user.is_authenticated:
                foods = request.user.profile.favorite_foods.all()
                context_dict['favorite_foods'] = foods
            return render(request, self.template_name, context_dict)

    @staticmethod
    def nutriscore_list(nutriscore):
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

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class ProductView(View):
    """Return the template for a single product"""
    template_name = 'core/product.html'

    def get(self, request, id):
        food = Food.objects.get(id=id)

        context_dict = {'food': food}

        return render(request, self.template_name, context_dict)


class FavoriteFoodView(View):
    """Return a template filled with all the foods a user saved.
    Only works if user is logged in"""
    template_name = 'core/favorite.html'

    @method_decorator(login_required)
    def post(self, request):
        food_id = request.POST['food_id']
        user = request.user
        if user.profile.favorite_foods.filter(id=food_id).count() == 1:
            return JsonResponse({'status': 'allready_faved'})
        elif user.profile.favorite_foods.filter(id=food_id).count() == 0:
            user.profile.favorite_foods.add(food_id)
            return JsonResponse({'status': 'ok'})

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        page = request.GET.get('page')
        queryset = user.profile.favorite_foods.all()

        if queryset.count() == 0:
            return render(request, self.template_name)
        else:
            new_queryset = []
            for list in self.chunks(queryset, 3):
                new_queryset.append(list)

            paginator = Paginator(new_queryset, 10)
            foods = paginator.get_page(page)
            context_dict = {"queryset": foods}
            return render(request, self.template_name, context_dict)

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class LegalNoticeView(View):
    """Return the legal notice template"""
    template_name = 'core/legal_notice.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    """Redirect the user to the contact me section in the home page"""

    def get(self, request):
        return redirect(reverse('core:home') + '#contact')
