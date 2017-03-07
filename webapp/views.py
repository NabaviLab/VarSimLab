from django.shortcuts import render
from django.http import StreamingHttpResponse
from easyscnvsim import settings
from scnvsim import run_simulation


def home(request):
    context = {'reference_ready': settings.REFERENCE_READY}
    return render(request, 'webapp/index.html', context)


def simulation_log(request):
    return StreamingHttpResponse(run_simulation())