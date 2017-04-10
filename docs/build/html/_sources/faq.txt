FAQs
----

1. What is Docker?
^^^^^^^^^^^^^^^^^^
Docker is the world's leading software containerization platform. Docker containers wrap a piece of software in a complete filesystem that contains everything needed to run: code, runtime, system tools, system libraries – anything that can be installed on a server. This guarantees that the software will always run the same, regardless of its environment.

read more on Docker website: http://www.docker.com

2. How is Docker different from a Virtual Machine (VM)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The below image summarizes how Docker is different from virtual machines from a technical point of view. Docker is very lightweight compared to a virtual machine, which makes it the ideal solution for wrapping software dependencies in a standard unit that runs on any machine where Docker engine is installed. Containers running on a single machine share the same operating system kernel; they start instantly and use less RAM. Images are constructed from layered filesystems and share common files, making disk usage and image downloads much more efficient.

.. image:: /images/figure-1.png


3. Do I need to learn a new platform to run the simulator?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**NO**. VarSimLab has a web interface that does the dirty work for you. The pipeline is fully automated from A to Z.

4. Do I need to be a Docker expert to use VarSimLab?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**NO**. You run only one command to get the application running. If you are using one of our hosted reference genomes at http://nabavilab.uconn.edu/datasets/varsimlab , you will just need to execute the file `./run.sh` and go to your web browser to initiate simulaitons.

5. My simulation is too slow. What should I do?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There may be several legitimate reasons for that:

- **The size of the genome is big:** For example, using the whole human genome (~3GB) takes time for processing variations and generating reads for that size of a file. Just give the simulator its time to go through all the pipeline steps. We recommend to use one chromosome at a time when you need to simulate the variations in large genomes.

- **Using Mac or Windows?** Make sure to properly increase the amount of memory and CPU available to Docker daemon. By default, when installing Docker on Windows or Mac, it is configured to have a limit of 2GB of RAM and 2 CPU cores to use across all running containers. Use the instructions here: https://docs.docker.com/docker-for-mac/#advanced for Mac and https://docs.docker.com/docker-for-windows/#advanced for Windows.