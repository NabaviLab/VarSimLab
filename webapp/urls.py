from django.conf.urls import url

import views

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]