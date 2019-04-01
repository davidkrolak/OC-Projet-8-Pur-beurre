import django

django.setup()

import requests
from core.models import Categories, Food


def api_categories_request():
    request_link = "https://fr.openfoodfacts.org/categories&json=1"
    request = requests.get(request_link)
    request_dict = request.json()

    print('OpenFoodFacts categories json requested\n---\n')
    return request_dict


def save_categories_into_db(request_dict, amount_of_cats):
    if amount_of_cats < request_dict['count']:
        for category in range(0, amount_of_cats):
            name = str(request_dict["tags"][category]["name"])
            url = str(request_dict["tags"][category]["url"])
            product_amount = int(request_dict["tags"][category]["products"])

            entry = Categories()
            entry.name = name
            entry.url = url
            entry.product_count = product_amount
            entry.clean()
            entry.save()

    elif amount_of_cats >= request_dict['count']:
        for category in range(0, request_dict['count']):
            name = str(request_dict["tags"][category]["name"])
            url = str(request_dict["tags"][category]["url"])
            product_amount = int(request_dict["tags"][category]["products"])

            entry = Categories()
            entry.name = name
            entry.url = url
            entry.product_count = product_amount
            entry.clean()
            entry.save()

    print('All categories inserted into db\n---\n')


def api_food_request(category_url, product_count):
    category_name = category_url.split("/")[-1]
    amount_of_pages = int(product_count / 1000)
    current_page = 1

    url = "https://fr.openfoodfacts.org/cgi/search.pl"

    params = {"action": "process",
              "tagtype_0": "categories",
              "tag_contains_0": "contains",
              "tag_0": category_name,
              "page_size": 1000,
              "page": current_page,
              "json": 1}

    request = requests.get(url, params)

    return request.json()


def save_food_into_db(request_dict):
    for food in range(0, request_dict["count"]):
        try:
            entry = Food()
            entry.name = request_dict["products"][food]["product_name"]
            entry.brand = request_dict["products"][food]["brands"]
            entry.nutriscore = request_dict["products"][food][
                "nutrition_grades"]
            entry.url = request_dict["products"][food]["url"]
            entry.clean()
            entry.save()
        except KeyError:
            pass

        for category in request_dict["products"][food]["categories"].split(
                ','):
            try:
                c = Categories.objects.get(name=category)
                entry.categories.add(c)
            except Categories.DoesNotExist:
                pass


if __name__ == '__main__':
    pass
