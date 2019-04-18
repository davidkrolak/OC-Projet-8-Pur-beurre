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
        response = self.client.get(reverse('core:home'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertTrue(html.endswith('</html>'))
        self.assertInHTML('http://testurl.com', html)


class PopulateDbTests(TestCase):
    """"""