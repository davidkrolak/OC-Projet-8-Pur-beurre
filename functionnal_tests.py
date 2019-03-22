import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class UserLoginTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_1(self):
        self.browser.get('http://localhost:8000/user/login/')
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')

        username_input.send_keys('test')
        password_input.send_keys('iamwrong')
        password_input.send_keys(Keys.ENTER)

        self.assertIn('Pur beurre - Connexion', self.browser.title)
