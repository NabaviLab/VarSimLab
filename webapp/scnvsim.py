from easyscnvsim import settings
from subprocess import Popen, PIPE, STDOUT
import os.path
import json


def _log(message):
    print("EasySCNVSim: " + str(message))


def check_reference_ready():
    """
    check if the reference folder is in place and all attributes are ready
    :return: nothing. Just set the parameter in settings appropriately
    """

    # check to see if there is a manifest file in the default reference path
    manifest_file = os.path.join(settings.DEFAULT_REFERENCE_PATH, 'manifest.json')
    if not os.path.isfile(manifest_file):
        _log("manifest.json file cannot be found in the reference folder; simulation will NOT work!")
        return

    _log("reading manifest.json ..")
    # read the manifest file
    with open(manifest_file, 'r') as manifest:
        data = json.load(manifest)
        reference_fasta = os.path.join(settings.DEFAULT_REFERENCE_PATH, data["reference"])

    if not os.path.isfile(reference_fasta):
        _log("genome reference file (.fasta | .fa) cannot be found in the reference folder; simulation will NOT work!")
        return

    _log("found all required simulation files in place; simulation is READY!")

    settings.REFERENCE_READY = True
    settings.INPUT_FILES = {"reference": reference_fasta}


def run_simulation():
    welcome_message = "***********************************************<br>"
    welcome_message += "*****DON'T CLOSE THIS BROWSER WINDOW*****<br>"
    welcome_message += "******UNTIL SIMULATION IS COMPLETED********<br>"
    welcome_message += "***********************************************<br><br>"
    welcome_message += "Starting Simulation ..<br><br>"
    welcome_message += "Simulation Parameters:<br>"
    for key, value in settings.SIMULATION_PARAMETERS.iteritems():
        welcome_message += "<b>" + key + "</b>: " + value + "<br>"
    welcome_message += "<br>"
    welcome_message += "Started ..<br><br>"
    yield welcome_message

    # create normal folder

    # copy normal genome there

    # create tumor folder

    # copy the normal genome there

    # simulate the tumor genome there

    # delete the normal genome from the tumor folder

    # generate reads in the normal folder

    # generate reads in the tumor folder

    # bye bye

    '''
    # create folder
    command = 'mkdir -p ' + settings.DEFAULT_REFERENCE_PATH + settings.SIMULATION_PARAMETERS['output-prefix'].strip() + '/normal'
    p = Popen(command , \
              stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    command = 'mkdir -p ' + settings.DEFAULT_REFERENCE_PATH + settings.OUTPUT_FOLDER.strip() + '/tumor'
    p = Popen(command , \
              stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    yield 'Started simulating SNPs, Indels, CNVs ..'

    command = '/easyscnvsim_lib/SInC/SInC_simulate ' + settings.INPUT_FILES['reference']

    p = Popen(command , \
              stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    '''


    # generate short reads
    # to be continued