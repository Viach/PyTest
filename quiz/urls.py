from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'quiz', views.quiz, name='quiz'),
    url(r'useful_links', views.useful_links, name='useful_links'),
]
