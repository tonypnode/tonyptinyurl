from django.db import models


class Urls(models.Model):
    url_string = models.URLField(blank=False)
    url_count = models.PositiveIntegerField(default=0)
    url_date_created = models.DateField(auto_now=True)

