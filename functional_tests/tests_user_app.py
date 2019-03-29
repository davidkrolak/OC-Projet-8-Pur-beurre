import time

from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SignUpTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_signup_form_submission_with_button(self):
        # Open a selenium browser & retrieve the forms elements we want to test
        self.browser.get(str(self.live_server_url) + '/user/signup/')
        username_input = self.browser.find_element_by_id('id_username')
        email_input = self.browser.find_element_by_id('id_email')
        first_name_input = self.browser.find_element_by_id('id_first_name')
        last_name_input = self.browser.find_element_by_id('id_last_name')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        submission_button = self.browser.find_element_by_class_name(
                'btn-primary')

        username_input.send_keys('test_username')
        email_input.send_keys('email@test.com')
        first_name_input.send_keys('test_first_name')
        last_name_input.send_keys('test_last_name')
        password1_input.send_keys('i_am_a_test_password_1234')
        password2_input.send_keys('i_am_a_test_password_1234')
        submission_button.click()
        time.sleep(0.5)
        redirection_url = self.browser.current_url

        self.assertEqual(self.live_server_url + '/user/account/',
                         redirection_url)

    def test_signup_form_submission_with_enter_keys(self):
        # Open a selenium browser & retrieve the forms elements we want to test
        self.browser.get(str(self.live_server_url) + '/user/signup/')
        username_input = self.browser.find_element_by_id('id_username')
        email_input = self.browser.find_element_by_id('id_email')
        first_name_input = self.browser.find_element_by_id('id_first_name')
        last_name_input = self.browser.find_element_by_id('id_last_name')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')

        username_input.send_keys('test_username')
        email_input.send_keys('email@test.com')
        first_name_input.send_keys('test_first_name')
        last_name_input.send_keys('test_last_name')
        password1_input.send_keys('i_am_a_test_password_1234')
        password2_input.send_keys('i_am_a_test_password_1234')
        password2_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
        redirection_url = self.browser.current_url

        self.assertEqual(self.live_server_url + '/user/account/',
                         redirection_url)


class ConnectionTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create_user(username='test',
                                 password='test1234',
                                 email='test@mail.com',
                                 first_name='test_first_name')

    def tearDown(self):
        self.browser.quit()

    def test_login_form_submission_with_button(self):
        # Open a selenium browser & retrieve the forms elements we want to test
        self.browser.get(str(self.live_server_url) + '/user/login/')
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
                'btn-primary')

        # Fill the forms input and click the submit button
        username_input.send_keys('test')
        password_input.send_keys('test1234')
        submission_button.click()
        time.sleep(0.5)
        redirection_url = self.browser.current_url

        # Check if the after the form validation match the valid redirection
        # url
        self.assertEqual(self.live_server_url + '/', redirection_url)

    def test_login_form_submission_with_enter_keys(self):
        # Open a selenium browser & retrieve the forms elements we want to test
        self.browser.get(str(self.live_server_url) + '/user/login/')
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
                'btn-primary')

        # Fill the forms input and click the submit button
        username_input.send_keys('test')
        password_input.send_keys('test1234')
        password_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
        redirection_url = self.browser.current_url

        # Check if the after the form validation match the valid redirection
        # url
        self.assertEqual(self.live_server_url + '/', redirection_url)
