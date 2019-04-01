from django.test import TestCase
from unittest.mock import MagicMock, patch

from core.populate_database import requests
from core import populate_database

from core.models import Categories, Food


class PopulateDatabaseScriptTests(TestCase):
    """"""

    @patch.object(requests, 'get')
    def test_request_categories_function_return_dict(self, mock_requests_get):
        """"""
        mock_requests_get.return_value = requests.Response()
        mock_requests_get.return_value._content = b'{"test":"test"}'
        request_dict = populate_database.api_categories_request()

        self.assertTrue(type(request_dict) is dict, 'yes')

    def test_right_amount_of_cats_in_db_lower_than_count(self):
        request_dict = {"tags": [{"name": "test1",
                                  "url": "urltest1",
                                  "products": "5"},
                                 {"name": "test2",
                                  "url": "urltest2",
                                  "products": "5"}],
                        "count": 2}
        populate_database.save_categories_into_db(request_dict, 1)

        self.assertEqual(Categories.objects.count(), 1)

    def test_right_amount_of_cats_in_db_higher_than_count(self):
        request_dict = {"tags": [{"name": "test1",
                                  "url": "urltest1",
                                  "products": "5"},
                                 {"name": "test2",
                                  "url": "urltest2",
                                  "products": "5"}],
                        "count": 2}
        populate_database.save_categories_into_db(request_dict, 5)

        self.assertEqual(Categories.objects.count(), 2)

    def test_api_food_request(self):
        """"""
        category = Categories()
        category.name = "Aliments et boissons à base de végétaux"
        category.url = "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux"
        category.product_count = 58226
        category.clean()
        category.save()

        populate_database.api_food_request(category.url,
                                           category.product_count)
