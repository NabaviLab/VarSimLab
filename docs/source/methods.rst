Simulator Methods
-----------------

The full source code of the project can be found on GitHub at `https://github.com/NabaviLab/VarSimLab <https://github.com/NabaviLab/VarSimLab>`_

1. Simulating SNPs, Indels and CNVs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This step uses `SInC <https://sourceforge.net/projects/sincsimulator/>`_
There are several advantages to this tool over similar error generators-- its speed, its ability to simulate a wider variety of errors (SNPs, INDELS, and CNVs), and the biologically realistic nature of the errors it generates. 

*Pattnaik, Swetansu, et al. "SInC: an accurate and fast error-model based simulator for SNPs, Indels and CNVs coupled with a read generator for short-read sequence data." BMC bioinformatics 15.1 (2014): 40.*

2. Simulating Tumors
^^^^^^^^^^^^^^^^^^^^
Tumor Ploidy is implemented by re-running SInC to generate more than 2 alleles. Tumor subclone is done by iteratively going through all above simulation steps to generate different aberrant genomes for different subclones.


3. Generating Short Reads
^^^^^^^^^^^^^^^^^^^^^^^^^
This step utilizes `ART articifial read generator <https://www.niehs.nih.gov/research/resources/software/biostatistics/art/index.cfm>`_
This is a widely used read generator with the capacity to faithfully simulate the error profiles of current next generation sequencers

*Huang, W., Li, L., Myers, J. R., & Marth, G. T. (2012). ART: a next-generation sequencing read simulator. Bioinformatics, 28(4), 593–594. http://doi.org/10.1093/bioinformatics/btr708*

