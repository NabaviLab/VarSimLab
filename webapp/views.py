from django.shortcuts import render
from django.http import StreamingHttpResponse
from subprocess import Popen, PIPE, STDOUT
from easyscnvsim import settings


def hello():
    p = Popen('java -jar /Users/abdelrahman/Downloads/scnvsim_1.3.1/normgenomsim_1.3.1.jar -o /Users/abdelrahman/Desktop/test -v /Users/abdelrahman/Desktop/hg19/chrom_lengths_hg19.txt -n /Users/abdelrahman/Desktop/hg19/hg19.fa' , \
              stdout = PIPE, stderr = STDOUT, shell = True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'


# Create your views here.
def home(request):
    context = {'reference_ready': settings.REFERENCE_READY}
    return render(request, 'webapp/index.html', context)


def simulation_log(request):
    return StreamingHttpResponse(hello())