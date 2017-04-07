Local Installation
-------------------
**NOTE:** If you are going to use the online version of AlgoPiper, ignore this section!

Thanks to the distributed architecture of the tool, AlgoManager and AlgoPiper can run on two different machines (locally or remotely).

Install Prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^
The only prerequisite is the Docker Engine: Follow the instructions on: https://docs.docker.com/engine/installation/


Download AlgoManager
^^^^^^^^^^^^^^^^^^^^^^^^
1. Clone AlgoManager repository https://github.com/algorun/algomanager
2. Navigate to the downloaded folder.
3. Run the script ``run.sh``
4. Go to http://localhost:8080 and make sure it is working

Configuring the Production Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to set AlgoManager on a shared server, edit ``algomanager/settings.py`` file. Change ``SERVER_PATH = 'http://localhost'`` to ``SERVER_PATH = 'http://server_IP'``

Add Available Algorithms
^^^^^^^^^^^^^^^^^^^^^^^^
Now, let AlgoManager be aware of what algorithms (AlgoRun containers) are available on your machine (or server).

1. Run docker ``exec -it algomanager bash``
2. Run ``python manage.py createsuperuser``. This will prompt you to create an admin user to manage the available algorithms on this algomanager instance.
3. Now exit this bash using ``exit``. Go to http://localhost:8080/admin/. Enter your newly created username and password. After you login, click on +Add, right beside Available Algorithms. Enter the name of the algorithm and its AlgoRun container. For example: *Name=REACT* and *Docker Image=algorun/react:latest*. Don't forget to ``docker pull`` those images from Docker Hub, before you make them available.

Run AlgoPiper
^^^^^^^^^^^^^
AlgoPiper is available as a Docker image on Docker Hub.

To run an instance of it, use ``docker run -p 8081:8765 -e MANAGER=<algomanager_url> algorun/algopiper``, where ``<algomanager_url>`` is the url where AlgoManager is running. Now, navigate to http://localhost:8081 to use it.

Congraulations! You now have a fully working version of AlgoPiper :)