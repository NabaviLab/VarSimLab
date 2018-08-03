FAQs
----

1. What is VarSimLab necessary?
^^^^^^^^^^^^^^^^^^
There are a variety of tools available for variant simulation, and short read simulation. However, generating benchmark ready simulated datasets remains an arduous process, requiring the use of multiple tools in conjuction. This is especially true for exome seqnuencing. The typical workflow for generating whole exome simulated data is approximately as follows: 
1) Exonic sequences have to be combined to use as input to an error simulator.
2)  The resulting error containing exome can then be used as input to a short read simulator 
3) the read simulator output is aligned back to the genome. 
4) The error simulator’s variant positions file is corrected to be relative to the genome, rather than relative to the exome.

Only then can the simulated data be used for benchmarking. The above pipeline, which requires at minimum 3 seperate tools, can be reduced into a single command with VarSimLab

.. code-block:: python
   python3 output_directory input_fasta.fa exons.bed -bam  

2 I want to perform exonic sequencing of a human sequence. How should I generate the bed file of exonic positions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fortunately `USCS tablebrowser  <https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=684589671_VNv2vSQOiC5FAMfrRqImSTiU0ab1>`_ makes this easy. See the docs here for a walkthrough
`here <https://github.com/NabaviLab/VarSimLab>`_

3 How can I simulate the exome of multiple chromosomes. 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As of the current release, unfortunately, exome simulation must be run one chromosome at a time, with one bed file per chromosome. Whole genome sequencing can accommodate multiple chromosomes

4 I have a question not covered here, or I've found a bug
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
please email us at thomas.davis@uconn.edu or abdelrahman.hosny@ieee.org

