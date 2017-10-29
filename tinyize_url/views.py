from django.shortcuts import render, redirect
from tinyize_url import codec62 as codec, models


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
    new_url = models.Urls.objects.create(url_string=request.POST['id_url_text'])
    html = 'http://127.0.0.1:8000/{}'.format(str(codec.encode(new_url.id)))
    return render(request, 'returned.html', {'tiny_url': html})
