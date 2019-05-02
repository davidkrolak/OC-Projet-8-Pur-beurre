from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm


class SignupViewTest(TestCase):
    """"""

    def setUp(self):
        self.form_data = {'username': 'test_form',
                          'last_name': 'form',
                          'first_name': 'test',
                          'email': 'test_form@mail.com',
                          'password1': 'iamnotsecure12',
                          'password2': 'iamnotsecure12'}

    def test_get_request_correct_html(self):
        response = self.client.get(reverse('user:signup'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertInHTML('<h2 class="text-center">Créer un compte</h2>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_post_request_redirection_correct_form(self):
        response = self.client.post(reverse('user:signup'), self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/account/')

    def test_post_request_redirection_wrong_form(self):
        form_data = self.form_data
        form_data['password2'] = 'iamwrong'
        response = self.client.post(reverse('user:signup'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, '/user/signup/')


class ConnectionViewTest(TestCase):
    """"""

    def setUp(self):
        User.objects.create_user(username='test',
                                 password='test1234',
                                 email='test@mail.com',
                                 first_name='test_first_name')
        self.credentials = {'username': 'test',
                            'password': 'test1234'}

    def test_user_login(self):
        response = self.client.post(reverse('user:login'), self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, 'test')

    def test_login_wrong_credentials(self):
        credentials = self.credentials
        credentials['password'] = 'iamwrong'
        response = self.client.post(reverse('user:login'), credentials)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, '')


class DisconnectionViewTest(TestCase):
    """"""

    def setUp(self):
        User.objects.create_user(username='test',
                                 password='test1234',
                                 email='test@mail.com',
                                 first_name='test_first_name')
        self.client.login(username='test', password='test1234')

    def test_user_logout(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, '')


class AccountViewTest(TestCase):
    """"""

    def setUp(self):
        User.objects.create_user(username='test',
                                 password='test1234',
                                 email='test@mail.com',
                                 first_name='test_first_name')

    def test_display_user_info(self):
        self.client.login(username='test', password='test1234')
        response = self.client.get(reverse('user:account'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, 'test')
        self.assertInHTML('<h2 class="text-black-50">test@mail.com</h2>', html)
        self.assertInHTML('<h2 class="section_title '
                          'text-center">test_first_name</h2>', html)

    def test_redirection_if_not_logged_in(self):
        response = self.client.get(reverse('user:account'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual('/user/login/?next=/user/account/', response.url)


class SignupFormTest(TestCase):

    def test_class_attributes(self):
        form = SignUpForm()
        self.assertIn('class="form-control"', form.as_p())

    def test_form_inputs(self):
        form = SignUpForm()
        self.assertIn('id="id_username"', form.as_p())
        self.assertIn('id="id_first_name"', form.as_p())
        self.assertIn('id="id_last_name"', form.as_p())
        self.assertIn('id="id_email"', form.as_p())
        self.assertIn('id="id_password1"', form.as_p())
        self.assertIn('id="id_password2"', form.as_p())


class LoginFormTest(TestCase):

    def test_class_attributes(self):
        form = LoginForm()
        self.assertIn('class="form-control"', form.as_p())

    def test_form_inputs(self):
        form = LoginForm()
        self.assertIn('id="id_username"', form.as_p())
        self.assertIn('id="id_password"', form.as_p())
