Simulator Methods
-----------------

The full source code of the project can be found on GitHub at `https://github.com/NabaviLab/VarSimLab <https://github.com/NabaviLab/VarSimLab>`_

1. The Docker Package
^^^^^^^^^^^^^^^^^^^^^
The web application is written in `Python Django <https://www.djangoproject.com/>`_ . The pipeline is a sequence of shell scripts used according to the simulation parameters. The package is built with `Docker <https://www.docker.com>`_

2. Simulating SNPs, Indels and CNVs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This step uses `SInC <https://sourceforge.net/projects/sincsimulator/>`_

*Pattnaik, Swetansu, et al. "SInC: an accurate and fast error-model based simulator for SNPs, Indels and CNVs coupled with a read generator for short-read sequence data." BMC bioinformatics 15.1 (2014): 40.*

3. Simulating Tumors
^^^^^^^^^^^^^^^^^^^^
Tumor Ploidy is implemented by re-running SInC to generate more than 2 alleles. Tumor subclone is done by iteratively going through all above simulation steps to generate different aberrant genomes for different subclones.


4. Generating Short Reads
^^^^^^^^^^^^^^^^^^^^^^^^^
This step utilizes `Wessim <https://github.com/sak042/Wessim>`_

*Kim, Sangwoo, Kyowon Jeong, and Vineet Bafna. "Wessim: a whole-exome sequencing simulator based on in silico exome capture." Bioinformatics (2013): btt074.*

