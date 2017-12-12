from django.test import TestCase
from tinyize_url.codec62 import encode, decode
from tinyize_url.models import Urls
from tinyize_url.tiny_helpers import check_duplicate


class TestBaseClass(TestCase):
    """
    Base test class for unit tests

    Sets up test cases used across multiple test classes
    """

    def setUp(self):
        """
        Setup common use cases and data for subclassed tests

        """
        self.test_url = 'http://www.abcdelsjfkd.tonypnode'

        self.test_input = {
            1: '1',
            100: '1C',
            1000: 'g8',
            10000: '2Bi',
        }

        self.post_data = {
            'id_url_text': self.test_url
        }


class HTMLPageTest(TestBaseClass):
    """
    Validates templates and redirects

    """

    def test_home_page_returns_correct_template(self):
        """
        Test proper template for home page

        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_return_page_returns_correct_template(self):
        """
        Test proper template for displaying a the tinyURL after input

        """
        response = self.client.post('/add_url', data=self.post_data, follow=True)
        self.assertTemplateUsed(response, 'returned.html')

    def test_redirect(self):
        """
        Test redirect response when requesting tiny URL

        """
        pass


class DatabaseTest(TestBaseClass):
    """
    Validates database functionality

    """

    def test_can_add_to_db(self):
        """
        Tests adding record to Url table

        """
        add_url = Urls.objects.create(url_string=self.test_url)
        add_url.save()
        self.assertEqual(self.test_url, Urls.objects.get(url_string=self.test_url).url_string)

    def test_for_duplicate(self):
        """
        Tests denying duplicate records in database

        """
        # TODO: Should the 'not_duplicate' check stay here? Or should it be a separate test?

        not_dup = check_duplicate(self.test_url)
        self.assertEqual(not_dup[0], False)
        add_url = Urls.objects.create(url_string=self.test_url)
        add_url.save()
        dup = check_duplicate(self.test_url)
        self.assertEqual(dup[0], True)


class UrlEncodingTests(TestBaseClass):
    """
    Validates encoding and decoding to Base62 functionality
    """

    def test_encode(self):
        """
        Validate the encoding output is correct

        """

        for int_in, str_out in self.test_input.items():
            self.assertEqual(encode(int_in), str_out)

    def test_decode(self):
        """
        Validate the decoding output is correct

        """

        for int_in, str_out in self.test_input.items():
            self.assertEqual(decode(str_out), int_in)


class MinorFeatures(TestBaseClass):
    """
    Validates minor feature functionality outside of primary function (adding URLs and redirecting)

    """

    def test_url_count_increase(self):
        """
        Test tracking usage of TinyURLs

        """
        add_url = Urls.objects.create(url_string=self.test_url)
        add_url.save()

        self.client.get('/go/{}'.format(encode(add_url.id)))
        self.client.get('/go/{}'.format(encode(add_url.id)))
        self.assertEqual(Urls.objects.get(id=decode(str(add_url.id))).url_count, 2)
