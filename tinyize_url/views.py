from django.shortcuts import render, redirect
from tinyize_url import codec62 as codec, models
import re


def home(request):
    return render(request, 'home.html')


def add_url(request):
    """
    This is where the magic happens
    - The URL in the textbox added to the database
        with an ID. that ID number is converted to base62
        and becomes the url.

    """
    # TODO: Should this query the DB for duplicate
    #       ... probably.
    print(request.POST['id_url_text'])
    new_url = models.Urls.objects.create(url_string=request.POST['id_url_text'])
    html = 'http://127.0.0.1:8000/go/{}'.format(str(codec.encode(new_url.id)))
    return render(request, 'returned.html', {'tiny_url': html})


def follow(request):
    """
    Query the DB for the url string (everything after 'go/' and
    redirect to the string in the
    :param request:
    :return:
    """
    html = request.get_full_path()
    url = models.Urls.objects.get(id=codec.decode(html.lstrip('/go/')))
    return redirect(url.url_string)
    # return render(request, 'returned.html', {'tiny_url': url.url_string})
