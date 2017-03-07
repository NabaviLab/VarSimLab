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
        repeat_mask = os.path.join(settings.DEFAULT_REFERENCE_PATH, data["repeat_mask"])
        chromosome_lengths = os.path.join(settings.DEFAULT_REFERENCE_PATH, data["chromosome_lengths"])

    if not os.path.isfile(reference_fasta):
        _log("genome reference file (.fasta | .fa) cannot be found in the reference folder; simulation will NOT work!")
        return

    if not os.path.isfile(repeat_mask):
        _log("repeat mask file (rmsk.txt) cannot be found in the reference folder; simulation will NOT work!")
        return

    if not os.path.isfile(chromosome_lengths):
        _log("chromosome lengths file (chrom_lengths_*.txt) cannot be found in the reference folder; simulation will NOT work!")
        return

    _log("found all required simulation files in place; simulation is READY!")

    settings.REFERENCE_READY = True
    settings.INPUT_FILES = {"reference": reference_fasta, \
                            "repeat_mask": repeat_mask, \
                            "chromosome_lengths": chromosome_lengths}


def run_simulation():
    #p = Popen('java -Xmx8g -jar /Users/abdelrahman/Downloads/scnvsim_1.3.1/normgenomsim_1.3.1.jar -o /Users/abdelrahman/Desktop/test -v /Users/abdelrahman/Desktop/hg19/chrom_lengths_hg19.txt -n /Users/abdelrahman/Desktop/hg19/hg19.fa' , \
    #          stdout=PIPE, stderr=STDOUT, shell=True)
    p = Popen('/lib/art_illumina' , \
              stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'