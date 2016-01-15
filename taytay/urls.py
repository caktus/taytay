"""taytay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^generate/$', views.song_generator, name='new-song'),
    url(r'^s/$', views.SongListView.as_view(), name='song-list'),
    url(r'^generate-cloud/$', views.word_frequencies, name='word-cloud'),
    url(r'^s/(?P<slug>\w{1,32})/$', views.song_detail, name='song-detail'),
    url(r'^$', views.HomepageView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
