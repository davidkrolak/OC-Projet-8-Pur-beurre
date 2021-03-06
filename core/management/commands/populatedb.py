import requests
from string import punctuation, digits
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError
from core.models import Categories, Food
from core.forms import CategoriesForm


class Command(BaseCommand):
    """Requests data to the OpenFoodFacts API to fill the local database
    with data (food, food categories)"""
    help = "populate the database via OpenFoodFacts API"

    def handle(self, *args, **options):
        self.stdout.write("Requesting categories to O.F.F.")
        categories_request_dict = self.api_categories_request()
        self.stdout.write("Saving categories into database")
        self.save_categories_into_db(categories_request_dict)

        cats_amount = 3

        categories = Categories.objects.all()

        for category in categories:
            self.stdout.write("Requesting items from {0}".format(
                    category.name))
            food_request_dict = self.api_food_request(category)
            self.stdout.write("inserting items from {0} into "
                              "database".format(
                    category.name))
            self.save_food_into_db(food_request_dict)
            cats_amount -= 1

    def api_categories_request(self):
        url = "https://fr.openfoodfacts.org/categories&json=1"

        request = requests.get(url)

        return request.json()

    def save_categories_into_db(self, request_dict):
        categories_list = request_dict["tags"][:3]
        for category in categories_list:
            name = self.string_cleaner(category["name"])
            url = category["url"]
            product_count = int(category["products"])
            off_id = category['id']

            form_dict = {'name': name,
                         'product_count': product_count,
                         'url': url,
                         'off_id': off_id}

            entry = CategoriesForm(form_dict)

            if entry.is_valid():
                entry.save()

    def api_food_request(self, category):
        url = "https://fr.openfoodfacts.org/cgi/search.pl"

        params = {"action": "process",
                  "tagtype_0": "categories",
                  "tag_contains_0": "contains",
                  "tag_0": category.off_id,
                  "page_size": 1000,
                  "json": 1}

        request = requests.get(url, params)

        return request.json()

    def save_food_into_db(self, request_dict):
        food_list = request_dict["products"]

        for food in food_list:
            food_name = self.string_cleaner(food["product_name"])
            try:
                food_brand = self.string_cleaner(food["brands"].split(',')[0])
            except KeyError:
                pass
            try:
                food_nutriscore = self.string_cleaner(food["nutrition_grades"])
            except KeyError:
                food_nutriscore = "Z"
            try:
                food_fat = float(food["nutriments"]["fat_100g"])
            except (KeyError, TypeError, ValueError):
                food_fat = None
            try:
                food_saturated_fat = float(food["nutriments"][
                                               "saturated-fat_100g"])
            except (KeyError, TypeError, ValueError):
                food_saturated_fat = None
            try:
                food_sugars = float(food["nutriments"]["sugars_100g"])
            except (KeyError, TypeError, ValueError):
                food_sugars = None
            try:
                food_salt = float(food["nutriments"]["salt_100g"])
            except (KeyError, TypeError, ValueError):
                food_salt = None
            food_url = food["url"]
            try:
                food_image_url = food["image_url"]
            except KeyError:
                food_image_url = None

            food_categories = food["categories"].split(',')

            entry = self.create_food_entry_into_db(food_name,
                                                   food_brand,
                                                   food_nutriscore,
                                                   food_fat,
                                                   food_saturated_fat,
                                                   food_sugars,
                                                   food_salt,
                                                   food_url,
                                                   food_image_url)

            self.add_relationships_between_food_and_categories(food_categories,
                                                               entry)

    def create_food_entry_into_db(self, name, brand, nutriscore, fat,
                                  saturated_fat, sugars, salt, url,
                                  image_url):
        try:
            entry = Food()
            entry.name = name
            entry.brand = brand
            entry.nutriscore = nutriscore
            entry.fat = fat
            entry.saturated_fat = saturated_fat
            entry.sugars = sugars
            entry.salt = salt
            entry.url = url
            if image_url:
                entry.image_url = image_url
            entry.clean()
            entry.save()
            return entry
        except(IntegrityError, DataError):
            pass

    def add_relationships_between_food_and_categories(self, food_categories,
                                                      entry):
        try:
            for food_category in food_categories:
                food_category = self.string_cleaner(food_category)
                category = \
                    Categories.objects.get_or_create(name=food_category)[0]
                entry.categories.add(category)
        except (ValidationError, AttributeError):
            pass

    def string_cleaner(self, my_str):
        s = my_str
        for character in punctuation:
            my_str = my_str.replace(character, '')
        for character in digits:
            my_str = my_str.replace(character, '')

        my_str = my_str.title().strip()
        return my_str
