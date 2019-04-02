import django

django.setup()

import requests
from string import punctuation, digits
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError
from core.models import Categories, Food


def api_categories_request():
    url = "https://fr.openfoodfacts.org/categories&json=1"

    request = requests.get(url)

    return request.json()


def save_categories_into_db(request_dict):
    categories_list = request_dict["tags"]
    for category in categories_list:
        name = string_cleaner(category["name"])
        url = category["url"]
        product_amount = int(category["products"])

        try:
            entry = Categories()
            entry.name = name
            entry.url = url
            entry.product_count = product_amount
            entry.clean()
            entry.save()
        except (IntegrityError, DataError):
            pass


def api_food_request(category):
    category_url = category.url
    category_name = category_url.split("/")[-1]

    url = "https://fr.openfoodfacts.org/cgi/search.pl"

    params = {"action": "process",
              "tagtype_0": "categories",
              "tag_contains_0": "contains",
              "tag_0": category_name,
              "page_size": 1000,
              "json": 1}

    request = requests.get(url, params)

    return request.json()


def save_food_into_db(request_dict):
    food_list = request_dict["products"]

    for food in food_list:
        food_name = string_cleaner(food["product_name"])
        food_brand = string_cleaner(food["brands"].split(',')[0])
        try:
            food_nutriscore = string_cleaner(food["nutrition_grades"])
        except KeyError:
            food_nutriscore = "Z"
        food_url = food["url"]
        food_categories = food["categories"].split(',')

        entry = create_food_entry_into_db(food_name, food_brand,
                                          food_nutriscore,
                                          food_url)
        add_relationships_between_food_and_categories(food_categories, entry)


def create_food_entry_into_db(name, brand, nutriscore, url):
    try:
        entry = Food()
        entry.name = name
        entry.brand = brand
        entry.nutriscore = nutriscore
        entry.url = url
        entry.clean()
        entry.save()
        return entry
    except(IntegrityError, DataError):
        pass


def add_relationships_between_food_and_categories(food_categories, entry):
    try:
        for food_category in food_categories:
            food_category = string_cleaner(food_category)
            category = Categories.objects.get_or_create(name=food_category)[0]
            entry.categories.add(category)
    except (ValidationError, AttributeError):
        pass


def string_cleaner(my_str):
    s = my_str
    for character in punctuation:
        my_str = my_str.replace(character, '')
    for character in digits:
        my_str = my_str.replace(character, '')

    my_str = my_str.title().strip()
    return my_str


if __name__ == '__main__':
    print("Request categories to OpenFoodFacts.\n")

    categories_request_dict = api_categories_request()
    save_categories_into_db(categories_request_dict)

    categories = Categories.objects.all()
    x = 0
    amount_of_cats = 5
    for category in categories:
        if x == amount_of_cats:
            break

        print("""Retrieving food from "{0}" category.\n""".format(
                category.name))
        request_dict = api_food_request(category)

        print("Saving food into db.\n")
        save_food_into_db(request_dict)
        x += 1
