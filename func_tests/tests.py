from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import re
import os

MAX_WAIT = 5


class NewVisitorTest(StaticLiveServerTestCase):

    """
     -User gets Main page
     -Main page shows clutter free and clean
         url entry form and submit button
     -when user inputs http://www.google.com, user is given
         somewhat large text displays showing
         shortented url like "http://turl/XD4RD"
     -Also has button denoting a click to copy to clipboard
     -When the copied url is put in a new browser window,
         the user is taken to www.google.com

    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def go_to_page(self, send_keys=False):
        self.browser.get('http://127.0.0.1:8000')
        input_box = self.browser.find_element_by_id('id_url_entry')
        if send_keys:
            input_box.send_keys('http://www.google.com')
            input_box.send_keys(Keys.ENTER)

    def wait_for_url_returned(self, url_text):
        """
        will use the url_text param when the site gets moved from
        127.0.0.1

        :param url_text: the shortened url
        :type url_text: str
        """
        start_time = time.time()

        while True:
            try:
                returned_url = self.browser.find_element_by_id('returned_url')
                self.assertRegex(returned_url.text, r'^http:\/\/127\.0\.0\.1\:8000\/[a-zA-z0-9]*')
                return returned_url.text
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_gets_proper_main_page(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('TJPHQ Short URL', self.browser.title)
        self.browser.quit()

    def test_gets_short_url(self):
        self.go_to_page(send_keys=True)
        self.wait_for_url_returned("http://127.0.0.1:8000")

    def test_url_redirect_is_correct(self):
        """
        Should this be a unit test?
        """
        self.go_to_page(send_keys=True)
        check_url = self.wait_for_url_returned('bla')
        self.browser.get(check_url)
        start_time = time.time()
        while True:
            try:
                self.assertIn('Google', self.browser.title)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)



