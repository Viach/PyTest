"""pytest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
#from django.conf.urls import handler404, handler500


handler500 = 'quiz.views.error_500'
#handler400 = 'mysite.views.my_custom_bad_request_view'
#handler404 = 'mysite.views.my_custom_bad_request_view'

urlpatterns = [
    url(r'^', include('quiz.urls')),
    url(r'^admin/', admin.site.urls),
]