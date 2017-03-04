from django.conf.urls import url

import views
from scnvsim import check_reference_ready

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]

check_reference_ready()