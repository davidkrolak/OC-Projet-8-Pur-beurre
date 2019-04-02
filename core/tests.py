from django.test import TestCase
from unittest.mock import MagicMock, patch

from core.populate_database import requests
from core import populate_database

from core.models import Categories, Food


class PopulateDatabaseScriptTests(TestCase):
    """"""

    @patch.object(requests, 'get')
    def test_api_categories_request_return_dict(self, mock_requests_get):
        """"""
        mock_requests_get.return_value = requests.Response()
        mock_requests_get.return_value._content = b'{"test":"test"}'
        request_dict = populate_database.api_categories_request()

        self.assertTrue(type(request_dict) is dict, 'yes')

    def test_save_categories_into_db_right_amount(self):
        request_dict = {"tags": [{"name": "testone",
                                  "url": "http://urltest1.com",
                                  "products": "5"},
                                 {"name": "testtwo",
                                  "url": "http://urltest2.com",
                                  "products": "5"}],
                        "count": 2}
        populate_database.save_categories_into_db(request_dict)

    @patch.object(requests, 'get')
    def test_api_food_request_return_dict(self, mock_requests_get):
        """"""
        mock_requests_get.return_value = requests.Response()
        mock_requests_get.return_value._content = b'{"test":"test"}'

        category = Categories()
        category.name = "Aliments et boissons à base de végétaux"
        category.url = "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux"
        category.product_count = 58226
        category.clean()
        category.save()

        request_dict = populate_database.api_food_request(category)

        self.assertTrue(type(request_dict), dict)

    def test_save_food_into_db(self):
        """"""
        request_dict = {"products": [
            {"product_name": "testone",
             "brands": "brandsone",
             "nutrition_grades": "A",
             "url": "http://iamurlone.com",
             "categories": "Aliments et boissons à base de végétaux, "
                           "Nourriture"},
            {"product_name": "testtwo",
             "brands": "brandstwo",
             "url": "http://iamurltwo.com",
             "categories": "Aliments et boissons à base de végétaux, Nourriture, Ca rend Malade"}
        ]}

        populate_database.save_food_into_db(request_dict)
        self.assertEqual(Food.objects.count(), 2)