Simulator User Guide
--------------------
1. Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^
Varsimlab can be called from the command line using any python 3 version

Varsimlab uses art_illumina to generate short reads with realistic sequencing errors. The documentation is available `Here <https://www.niehs.nih.gov/research/resources/software/biostatistics/art/index.cfm>`_

To install ART 

.. code-block:: bash
 curl -O https://www.niehs.nih.gov/research/resources/assets/docs/artbinmountrainier2016.06.05linux64.tgz
 tar -xvzf artbinmountrainier2016.06.05linux64.tgz

VarSimLab uses SInC simulator to generate biologically realistic tumor genomic variations. The source files and instructions on compiling are available `Here <https://sourceforge.net/projects/sincsimulator/files/?source=navbar>`_

Lastly if you'd like to use Varsimlabs exome sequencing capabilities, Varsimlab uses Bedtools is required. bedtools documentation is available `Here <http://bedtools.readthedocs.io/en/latest/>`_

To install bedtools 

.. code-block:: bash
 wget https://github.com/arq5x/bedtools2/releases/download/v2.25.0/bedtools-2.25.0.tar.gz
 tar -zxvf bedtools-2.25.0.tar.gz
 cd bedtools2
 make
```


2. Prepare The Reference Genome
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two ways to easily run VarSimLab for a reference genome

1. Download a pre-prepared folder to use from http://nabavilab.uconn.edu/datasets/varsimlab/ .
2. Prepare your own reference (super easy).

To prepare a reference genome, follow these steps:

1. Create a new folder to hold your files.
2. Copy the reference genome in FASTA format (.FASTA | .FA ) to the folder. You can also download genome from UCSC Genome Browser https://genome.ucsc.edu/cgi-bin/hgGateway
3. Copy target regions file in BED format (.BED) to the folder. You can also download the target files from UCSC Table Browser https://genome.ucsc.edu/cgi-bin/hgTables. You can also see more information about preparing the bed file at our github repository https://github.com/NabaviLab/VarSimLab

That's it! Your reference is ready to generate reads from.

3. Running VarSimLab
^^^^^^^^^^^^^^^^^^^^
Here are the available arguments VarSimLab accepts at the command line
  required positional arguments:

  filename              name of output file
  genome                genome to be processessed

VarSimLab also requires one of the following arguments:

  -use_genome           generate tumor and normal for entire provided sequence.                         used for whole genome sequence simualtion
  -bed                  generate tumor and normal based on bed file containing
                        exonic regions. used for whole exome sequence simulation

read generation parameters:
  arguments to adjust read generation

  -c C                  read depth of coverage
  -s                    use single end reads (default paired)
  -l L                  read length. default 100 bp
  -m M                  maximum distance for two bed ranges to be merged into
                        one range. If zero, merges only those ranges that
                        directly overlap with each other

error parameters:
  arguments to adjust tumor error generation

  -cnv                  percent of total input to be incorporated into a CNV.
                        Values from 0 to 100. 4 would signify 4 percent of
                        input should be included in CNVs
  -cnv_min_size
                        minimum size of CNVs
  -cnv_max_size
                        CNV_max_size
  -snp                  percent of total input to be turned into SNPs. Values
                        from 0 to 100. A value of 5 indicates 5 percent of
                        genome should be turned into SNPs
  -indel                percent of total input to be included in INDELS.
                        values from 0 to 100, a value of 1 indicates 1 percent
                        of the genome should be included in indels



4. Understanding Simulator Results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two folders inside the `output_prefix` folder.

- **Normal:** it will contain `.FASTQ` file for reads that represent the control (or normal) sample. There will be two `.FASTQ` files if paired end reads were generated, and one if single end reads were generated.
- **Tumor:** it will contain `.FASTQ` file for reads that represent the tumor sample. There will be two `.FASTQ` files per allele for paired end sequencing, or one per allele for unpaired. In addition, it will contain the benchmark data that tells you where SNPs, Indels and CNVs for each allele in each subclone generated. 

5. Understanding Benchmarking files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If a bed file was supplied, two sets of positions are calculated, one relative to the genome, the other relative to the exome. The genome position is likely to be much greater than the exome position, since the exome is much smaller than the genome, and exons are usually surrounded by large noncoding stretches. 
