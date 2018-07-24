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

22 My simulation is too slow. What should I do?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There may be several legitimate reasons for that:

- **The size of the genome is big:** For example, using the whole human genome (~3GB) takes time for processing variations and generating reads for that size of a file. Just give the simulator its time to go through all the pipeline steps. We recommend to use one chromosome at a time when you need to simulate the variations in large genomes.

- **Using Mac or Windows?** Make sure to properly increase the amount of memory and CPU available to Docker daemon. By default, when installing Docker on Windows or Mac, it is configured to have a limit of 2GB of RAM and 2 CPU cores to use across all running containers. Use the instructions here: https://docs.docker.com/docker-for-mac/#advanced for Mac and https://docs.docker.com/docker-for-windows/#advanced for Windows.
