from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r"^quiz/(start|finish|next)", views.quiz, name='quiz'),
    url(r"^quiz_start", views.quiz_start, name='quiz_start'),
    url(r"^quiz_process", views.quiz_process, name='quiz_process'),
    url(r"^quiz_finish", views.quiz_finish, name='quiz_finish'),
    url(r'^useful_links', views.useful_links, name='useful_links'),
    url(r'^contact', views.contact, name='contact'),
]
