from easyscnvsim import settings
from subprocess import Popen, PIPE, STDOUT
import os
from os.path import isfile, join
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
        target_file = os.path.join(settings.DEFAULT_REFERENCE_PATH, data["targets"])

    if not os.path.isfile(reference_fasta):
        _log("genome reference file (.fasta | .fa) cannot be found in the reference folder; simulation will NOT work!")
        return

    if not os.path.isfile(target_file):
        _log("targets file (.bed) cannot be found in the reference folder; simulation will NOT work!")
        return

    _log("found all required simulation files in place; simulation is READY!")

    settings.REFERENCE_READY = True
    settings.INPUT_FILES = {"reference": data['reference'], "targets": data['targets']}


def run_simulation():
    simulation_parameters = settings.SIMULATION_PARAMETERS

    args = [settings.INPUT_FILES['reference'],
            settings.INPUT_FILES['targets'],
            simulation_parameters['output-prefix'],
            simulation_parameters['snp-rate'],
            simulation_parameters['indel-rate'],
            simulation_parameters['transition-transversion-ratio'],
            simulation_parameters['cnv-rate'],
            simulation_parameters['cnv-min-size'],
            simulation_parameters['cnv-max-size'],
            simulation_parameters['number-of-reads'],
            simulation_parameters['read-length'],
            simulation_parameters['ploidy'],
            simulation_parameters['subclones']]
    command = "nohup /easyscnvsim_lib/run.sh " + ' '.join(args) + " &"
    _ = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)

    web_message = '<b>Thank You For Choosing VarSimLab!</b><br><br>'
    web_message += 'Check the file ' + simulation_parameters['output-prefix'] + '/SIMULATION_IS_RUNNING.txt'
    web_message += ' for the simulation progress ..<br>'
    web_message += 'Once the simulation is complete, you will find a file ' + \
                   simulation_parameters['output-prefix'] + '/SIMULATION_IS_COMPLETE.txt'
    web_message += '<br><br>'
    web_message += 'You can close this window, and the simulation will still be working. \
    Follow up with the progress in the simulation progress file<br><br>'
    web_message += "You can also <a href='/'>go back</a> and run another simulation concurrently \
     by chancing the <i>Output Prefix</i> parameter and hit run again ..<br>"
    web_message += "WARNING: This simulation eats up large memory space. \
    Don't run multiple simulations unless you have enough RAM. You are advised to try only one simulation and \
     see how it goes first"
    return web_message
