from django.shortcuts import render
from easyscnvsim import settings


# Create your views here.
def home(request):
    context = {'reference_ready': settings.REFERENCE_READY}
    return render(request, 'webapp/index.html', context)
