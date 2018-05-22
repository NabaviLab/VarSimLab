from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from easyscnvsim import settings
from scnvsim import run_simulation
import random


def home(request):
    context = {'reference_ready': settings.REFERENCE_READY}
    return render(request, 'webapp/index.html', context)


def simulation(request):
    return HttpResponse(run_simulation())


@csrf_exempt
def params(request):
    sim_params = dict(request.POST.iterlists())
    for key, value in sim_params.iteritems():
        sim_params[key] = value[0]
    sim_params['output-prefix'] = sim_params['output-prefix'] + str(random.randint(1000,9999))
    settings.SIMULATION_PARAMETERS = sim_params

    return HttpResponse('ok')