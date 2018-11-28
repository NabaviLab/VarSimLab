VarSimLab Documentation
========================

Advances in next generation sequencing have led to the creation of many tools for detecting variations in tumor sequences. To evaluate the performance of these tools, researchers need articifial tumor sequences with known variant positions. Currently, generating such simulated datasets is possible, it requires significant labor and technical know-how. The benchmarking process is especially difficult for tools that call variants from tumor whole exome sequences, an increasingly popular technique for tumor characterization

VarSimLab is a tool designed to dramatically simplify varaint-caller benchmarking.  
As of the current version (**nabavilab/varsimlab:0.2**), the simulator generates realistic artificial short reads, which harbor structural and copy number variations. VarSimLab can also simulates tumor heterozygosity (Ploidy and Subclones), and can generate whole genome, or whole exome datasets.

The output of VarSimLab is a directory containing tumor and normal reads, a log file containing simulation information, and benchmarking files, with the locations and positions of all variants generated in the run. 
 
The output of VarSimLab ideal for benchmarking variant calling software, and showed high variant rediscovery rates for SNPs INDELS and CNVs when tested using VarScan variant calling software. 

.. toctree::
   :maxdepth: 3

   user-guide
   methods
   faq
   help

