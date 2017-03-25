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


def welcome_message(params):
    welcome_message = "***********************************************<br>"
    welcome_message += "*****DON'T CLOSE THIS BROWSER WINDOW*****<br>"
    welcome_message += "******UNTIL SIMULATION IS COMPLETED********<br>"
    welcome_message += "***********************************************<br><br>"
    welcome_message += "Starting Simulation ..<br><br>"
    welcome_message += "Simulation Parameters:<br>"
    for key, value in params.iteritems():
        welcome_message += "<b>" + key + "</b>: " + value + "<br>"
    welcome_message += "<br>"
    welcome_message += "Started ..<br><br>"
    yield welcome_message


def create_normal_folder(params):
    command = 'mkdir -p ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'
    yield 'Created a folder for normal reads ..<br>'
    yield 'Copying temporary files ..<br>'

    # copy the normal genome there
    command = 'cp ' + settings.DEFAULT_REFERENCE_PATH +  settings.INPUT_FILES['reference'] + ' ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/;'
    command += 'cp ' + settings.DEFAULT_REFERENCE_PATH +  settings.INPUT_FILES['targets'] + ' ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/;'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'


def create_tumor_folder(params):
    command = 'mkdir -p ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'
    yield 'Created a folder for tumor reads ..<br>'
    yield 'Copying temporary files ..<br>'

    # copy the normal genome there
    command = 'cp ' + settings.DEFAULT_REFERENCE_PATH + settings.INPUT_FILES['reference'] + ' ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/;'
    command += 'cp ' + settings.DEFAULT_REFERENCE_PATH + settings.INPUT_FILES['targets'] + ' ' + settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/;'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'


def simulate_tumor_genome(params):
    yield 'Simulating variations ..<br>'
    working_dir = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/'
    command = '/easyscnvsim_lib/SInC/SInC_simulate ' \
              + '-S ' + params['snp-rate'] + ' ' \
              + '-I ' + params['indel-rate'] + ' ' \
              + '-p ' + params['cnv-rate'] + ' ' \
              + '-l ' + params['cnv-min-size'] + ' ' \
              + '-u ' + params['cnv-max-size'] + ' ' \
              + '-t ' + params['transition-transversion-ratio'] + ' ' \
              + settings.INPUT_FILES['reference']
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    # delete the normal genome from the tumor folder
    yield '<br>Cleaning temporary files ..<br>'
    command = 'rm ' + settings.INPUT_FILES['reference']
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    # rename both allele files to be able to generate reads afterwards
    tumor_file = [f for f in os.listdir(working_dir) if isfile(join(working_dir, f))]
    for f in tumor_file:
        if "allele_1" in f:
            command = 'mv ' + f + ' allele_1.fa'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "allele_2" in f:
            command = 'mv ' + f + ' allele_2.fa'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "SNPs" in f and "_1.txt" in f:
            command = 'mv ' + f + ' SNPs_1.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "SNPs" in f and "_2.txt" in f:
            command = 'mv ' + f + ' SNPs_2.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "INDELs" in f and "_1.txt" in f:
            command = 'mv ' + f + ' INDEL_1.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "INDELs" in f and "_2.txt" in f:
            command = 'mv ' + f + ' INDELs_2.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "CNV" in f and "stdresults" in f:
            command = 'mv ' + f + ' CNV_stdresults.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'
        if "CNV" in f and "stdresults" not in f:
            command = 'mv ' + f + ' CNV_restuls.txt'
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
            while True:
                line = p.stdout.readline()
                if not line: break
                yield line + '<br>'


def generate_normal_reads(params):
    yield 'Generating normal reads ..<br>'
    working_dir = '/easyscnvsim_lib/Wessim/'
    reference = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/' + settings.INPUT_FILES['reference']
    targets = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/' + settings.INPUT_FILES['targets']
    output_prefix = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/normal'
    model_file = '/easyscnvsim_lib/Wessim/models/ill100v4_p.gzip'

    command = "python /easyscnvsim_lib/Wessim/Wessim1.py" \
                     + " -R " + reference \
                     + " -B " + targets \
                     + " -n " + params['number-of-reads'] \
                     + " -l " + params['read-length'] \
                     + " -M " + model_file \
                     + " -o " + output_prefix \
                     + " -t " + params['number-of-threads'] \
                     + " -p"
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'
    yield 'Finished generating normal reads ..<br>'


def generate_tumor_read(params):
    yield 'Generating tumor reads from allele 1 ..<br>'
    working_dir = '/easyscnvsim_lib/Wessim/'
    reference = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/allele_1.fa'
    targets = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/' + settings.INPUT_FILES['targets']
    output_prefix = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/tumor_allele1'
    model_file = '/easyscnvsim_lib/Wessim/models/ill100v4_p.gzip'

    command = "python /easyscnvsim_lib/Wessim/Wessim1.py" \
                     + " -R " + reference \
                     + " -B " + targets \
                     + " -n " + str(int(params['number-of-reads']) / 2) \
                     + " -l " + params['read-length'] \
                     + " -M " + model_file \
                     + " -o " + output_prefix \
                     + " -t " + params['number-of-threads'] \
                     + " -p"
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    reference = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/allele_2.fa'
    output_prefix = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/tumor_allele2'

    command = "python /easyscnvsim_lib/Wessim/Wessim1.py" \
                     + " -R " + reference \
                     + " -B " + targets \
                     + " -n " + str(int(params['number-of-reads']) / 2) \
                     + " -l " + params['read-length'] \
                     + " -M " + model_file \
                     + " -o " + output_prefix \
                     + " -t " + params['number-of-threads'] \
                     + " -p"
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'

    yield 'Finished generating tumor reads ..<br><br>'


def clean_tmp(params):
    yield '<br>Cleaning temporary files ..<br>'
    working_dir = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/tumor/'
    command = 'rm *.bed*;'
    command += 'rm ' + settings.INPUT_FILES['reference'] + '*'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'
    working_dir = settings.DEFAULT_REFERENCE_PATH + params['output-prefix'].strip() + '/normal/'
    command = 'rm *.bed*;'
    p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, cwd=working_dir)
    while True:
        line = p.stdout.readline()
        if not line: break
        yield line + '<br>'


def end_message():
    end_message = "<br><br>***********************************<br>"
    end_message += "******SIMULATIONCOMPLETED*****<br>"
    end_message += "***********************************<br>"
    yield end_message


def run_simulation():
    simulation_parameters = settings.SIMULATION_PARAMETERS

    # print welcome message
    for message in welcome_message(simulation_parameters):
        yield message

    # create normal folder
    for message in create_normal_folder(simulation_parameters):
        yield message

    # create tumor folder
    for message in create_tumor_folder(simulation_parameters):
        yield message

    # simulate the tumor genome there
    for message in simulate_tumor_genome(simulation_parameters):
        yield message

    # generate reads in the normal folder
    for message in generate_normal_reads(simulation_parameters):
        yield message

    # generate reads in the tumor folder
    for message in generate_tumor_read(simulation_parameters):
        yield message

    # clean temporary files
    for message in clean_tmp(simulation_parameters):
        yield message

    # bye bye
    for message in end_message():
        yield message
