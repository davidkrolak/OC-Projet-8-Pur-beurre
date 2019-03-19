from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SignupViewTest(TestCase):
    """"""

    def test_get_request_correct_html(self):
        response = self.client.get(reverse('user:signup'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<h2>Créer un compte</h2>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_post_request_redirection_correct_form(self):
        form_data = {'username': 'test_form',
                     'last_name': 'form',
                     'first_name': 'test',
                     'email': 'test_form@mail.com',
                     'password1': 'iamnotsecure12',
                     'password2': 'iamnotsecure12'}
        response = self.client.post(reverse('user:signup'), form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/account/')

    def test_post_request_redirection_wrong_form(self):
        form_data = {'username': 'test_form',
                     'last_name': 'form',
                     'first_name': 'test',
                     'email': 'test_form@mail.com',
                     'password1': 'iamnotsecure12',
                     'password2': 'iamwrong'}
        response = self.client.post(reverse('user:signup'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, '/user/signup/')


class AccountViewTest(TestCase):
    """"""

    def test_client_login(self):
        User.objects.create_user(username='test',
                                 password='test1234',
                                 email='test@mail.com')
        self.client.login(username='test', password='test1234')

        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf8'), 'test')
