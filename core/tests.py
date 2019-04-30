from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.urls import reverse

from .management.commands import populatedb
from .models import *


class HomeViewTests(TestCase):
    """"""

    def test_get_request_correct_html(self):
        response = self.client.get(reverse('core:home'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('''<h1 class="text-white">Du gras, oui, mais de 
        qualité</h1>''', html)


class ResearchViewTests(TestCase):
    """"""

    def setUp(self):
        Food.objects.create(name='testname',
                            brand='testbrand',
                            nutriscore='A',
                            url='http://testurl.com',
                            image_url='http://testimageurl.com')

    def test_get_request_got_results(self):
        form_data = {'food': 'test'}
        response = self.client.get(reverse('core:research'), form_data)
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('''
        <img src="http://testimageurl.com" alt="food_image" 
        class="food_image">''', html)

    def test_get_request_no_result(self):
        form_data = {'food': 'iamnotaresult'}
        response = self.client.get(reverse('core:research'), form_data)
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('<h1>Pas de résultats !</h1>', html)


class SubstituteViewTests(TestCase):
    """"""

    def setUp(self):
        c = Categories.objects.create(name='testcat',
                                      product_count=2,
                                      url='http://testcaturl.com',
                                      off_id='test')
        f1 = Food.objects.create(name='testname',
                                 brand='testbrand',
                                 nutriscore='B',
                                 url='http://testurl.com',
                                 image_url='http://testimageurl.com',
                                 id=1)
        f1.categories.add(c)
        f2 = Food.objects.create(name='testnametwo',
                                 brand='testbrandtwo',
                                 nutriscore='A',
                                 url='http://testurltwo.com',
                                 image_url='http://testimageurltwo.com',
                                 id=2)
        f2.categories.add(c)

    def test_get_request_got_results(self):
        response = self.client.get(reverse('core:substitute', args=[1]))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('''
        <img src="http://testimageurltwo.com" alt="food_image" 
        class="food_image">''', html)

    def test_get_request_no_results(self):
        response = self.client.get(reverse('core:substitute', args=[2]))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('<h1>Pas de résultats !</h1>', html)


class ProductViewTests(TestCase):
    """"""

    def setUp(self):
        Food.objects.create(name='testname',
                            brand='testbrand',
                            nutriscore='A',
                            url='http://testurl.com',
                            image_url='http://testimageurl.com')

    def test_get_request_correct_html(self):
        id = Food.objects.first().id
        response = self.client.get(reverse('core:product', args=[id]))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML("""
          <a href="http://testurl.com" class="btn btn-primary">Voir la fiche 
          d'OpenFoodFacts</a>
        """, html)


class FavoriteFoodViewTests(TestCase):
    """"""

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='test1234',
                                             email='test@mail.com',
                                             first_name='test_first_name')
        self.food = Food.objects.create(name='testname',
                                        brand='testbrand',
                                        nutriscore='A',
                                        url='http://testurl.com',
                                        image_url='http://testimageurl.com')

    def test_post_request_food_saved_user_logged_in(self):
        self.client.login(username='test', password='test1234')
        form_data = {"food_id": self.food.id}
        self.client.post(reverse('core:favorite'), form_data)

        self.assertEqual(self.user.profile.favorite_foods.count(), 1)
        self.assertEqual(self.user.profile.favorite_foods.first(), self.food)

    def test_post_request_try_to_fav_an_allready_faved_food(self):
        self.client.login(username='test', password='test1234')
        self.user.profile.favorite_foods.add(self.food)

        form_data = {"food_id": self.food.id}
        response = self.client.post(reverse('core:favorite'), form_data)

        self.assertEqual(self.user.profile.favorite_foods.count(), 1)
        self.assertEqual(self.user.profile.favorite_foods.first(), self.food)
        self.assertEqual(response.status_code, 200)

    def test_post_request_food_user_not_logged_in(self):
        form_data = {"food_id": self.food.id}
        self.client.post(reverse('core:favorite'), form_data)

        self.assertEqual(self.user.profile.favorite_foods.count(), 0)
        self.assertEqual(self.user.profile.favorite_foods.first(), None)


class LegalNoticeViewTests(TestCase):
    """"""

    def test_get_request_correct_html(self):
        response = self.client.get(reverse('core:legal_notice'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML(
                '''<h1 class="section_title text-center">Mentions Légales</h1>''',
                html)


class ContactViewTests(TestCase):
    """"""

    def test_get_request_correct_html(self):
        response = self.client.get(reverse('core:contact'))

        self.assertEqual(response.status_code, 302)


class PopulateDbTests(TestCase):
    """"""

    def setUp(self) -> None:
        self.command = populatedb.Command()

    @patch('requests.get')
    def test_api_categories_request(self, get):
        response = self.command.api_categories_request()
        self.assertTrue(get.called)

    def test_save_categories_into_db(self):
        request_dict = {'tags': [
            {'name': 'testname',
             'url': 'http://testurl.com',
             'products': 1,
             'id': 'testid'}
        ]}
        self.command.save_categories_into_db(request_dict)

        self.assertEqual(Categories.objects.count(), 1)

    @patch('requests.get')
    def test_api_food_request(self, get):
        category = MagicMock()
        category.off_id = 'test'

        response = self.command.api_food_request(category)
        self.assertTrue(get.called)

    def test_save_food_into_db(self):
        request_dict = {'products': [
            {'product_name': 'testname',
             'brands': 'testbrand',
             'nutrition_grades': 'A',
             'url': 'http://testurl.com',
             'image_url': 'http://testimageurl.com',
             'categories': 'testcatone, testcattwo'}
        ]}

        self.command.save_food_into_db(request_dict)

        f = Food.objects.first()
        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(f.categories.count(), 2)

    def test_save_food_into_db_no_nutriscore(self):
        request_dict = {'products': [
            {'product_name': 'testname',
             'brands': 'testbrand',
             'url': 'http://testurl.com',
             'image_url': 'http://testimageurl.com',
             'categories': 'testcatone, testcattwo'}
        ]}

        self.command.save_food_into_db(request_dict)

        f = Food.objects.first()
        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(f.categories.count(), 2)
        self.assertEqual(f.nutriscore, 'Z')

    def test_create_food_entry_into_db(self):
        name = 'testname'
        brand = 'testbrand'
        nutriscore = 'A'
        fat = 0.5
        saturated_fat = 1
        sugars = 2
        salt = 12.5
        url = 'http://testurl.com'
        image_url = 'http://testimageurl.com'

        self.command.create_food_entry_into_db(name, brand, nutriscore, fat,
                                               saturated_fat, sugars, salt,
                                               url, image_url)

        self.assertEqual(Food.objects.count(), 1)

    def test_add_relationships_between_food_and_categories(self):
        name = 'testname'
        brand = 'testbrand'
        nutriscore = 'A'
        url = 'http://testurl.com'
        image_url = 'http://testimageurl.com'
        categories = ['testcatone', 'testcattwo']
        entry = Food(name=name, brand=brand, nutriscore=nutriscore, url=url,
                     image_url=image_url)
        entry.save()

        self.command.add_relationships_between_food_and_categories(
                categories, entry)

        self.assertEqual(entry.categories.count(), 2)
