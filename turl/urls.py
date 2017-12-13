"""
turl URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin
from tinyize_url import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^add_url', views.add_url, name='add'),
    url(r'^go/[a-zA-z0-9][a-zA-z0-9]*?', views.follow),

]
