from django.test import TestCase
from tinyize_url.codec62 import encode, decode
from tinyize_url.models import Urls
from tinyize_url.tiny_helpers import check_duplicate


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class DatabaseTest(TestCase):

    def setUp(self):
        """
        Create test database?

        :return:
        """

        self.test_url = 'http://www.abcdelsjfkd.poop'
        pass

    def test_can_add_to_db(self):
        add_url = Urls.objects.create(url_string=self.test_url)
        add_url.save()
        self.assertEqual(self.test_url, Urls.objects.get(url_string=self.test_url).url_string)

    def test_for_duplicate(self):
        add_url = Urls.objects.create(url_string=self.test_url)
        add_url.save()
        response = check_duplicate(self.test_url)
        print(response)
        self.assertEqual(response[0], True)


class UrlEncodingTests(TestCase):

    def setUp(self):
        self.test_input = {
            1: '1',
            100: '1C',
            1000: 'g8',
            10000: '2Bi',
        }

    def test_encode(self):
        """
        validate the encoding output is correct

        """

        for int_in, str_out in self.test_input.items():
            self.assertEqual(encode(int_in), str_out)

    def test_decode(self):
        """
        Validate the decoding output is correct

        """

        for int_in, str_out in self.test_input.items():
            self.assertEqual(decode(str_out), int_in)


