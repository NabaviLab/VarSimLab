from django.conf.urls import url

import views
from scnvsim import check_reference_ready

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^simulation$', views.simulation, name='simulation'),
    url(r'^params$', views.params, name='params'),
]

check_reference_ready()