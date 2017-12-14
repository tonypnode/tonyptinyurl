from django.shortcuts import render, redirect
from tinyize_url import codec62 as codec, models
from tinyize_url import tiny_helpers as helpers


def home(request):
    return render(request, 'home.html')


def add_url(request):
    """
    This is where the magic happens
    - The URL in the textbox added to the database
        with an ID. that ID number is converted to base62
        and becomes the url.

    """
    html_base = 'http://127.0.0.1:8000/go/'
    posted_url = request.POST['id_url_text']
    if not posted_url and posted_url != '':
        # TODO: need helper that does both checks and checks for recursive url (/go/bla)
        check = helpers.check_duplicate(posted_url)
        if check[0]:
            url_id = check[1]
        else:
            new_url = models.Urls.objects.create(url_string=posted_url)
            url_id = new_url.id

        html = '{}{}'.format(html_base, str(codec.encode(url_id)))
    return render(request, 'returned.html', {'tiny_url': html})


def follow(request):
    """
    Query the DB for the url string (everything after 'go/' and
    redirect to the string in the full url in db

    :param request:
    :type request:

    :return: redirect

    """
    html = request.get_full_path().lstrip('/go/')
    url = models.Urls.objects.get(id=codec.decode(html))
    url.url_count += 1
    url.save()
    return redirect(url.url_string)
