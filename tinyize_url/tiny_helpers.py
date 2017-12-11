import tinyize_url.models as models


def check_duplicate(test_url):
    """
    Checks database if url is already present

    :param test_url: URL
    :type test_url: str

    :return: tuple
    """
    try:
        url = models.Urls.objects.get(url_string=test_url)
        return True, url.id
    except:
        return False, None
