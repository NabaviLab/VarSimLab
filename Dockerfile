FROM ahosny/python
LABEL MAINTAINER "Abdelrahman Hosny <abdelrahman.hosny@hotmail.com>"

ENV PYTHONUNBUFFERED 1

# install web app
RUN mkdir /easyscnvsim
WORKDIR /easyscnvsim
ADD requirements.txt /easyscnvsim/
RUN pip install -r requirements.txt

# ADD SCNVSim and ART
RUN apt-get update && apt-get install -y default-jre
ADD easyscnvsim_lib /easyscnvsim_lib

ADD easyscnvsim /easyscnvsim/easyscnvsim
ADD webapp /easyscnvsim/webapp
ADD manage.py /easyscnvsim/manage.py

EXPOSE 8000
ENTRYPOINT ["python", "/easyscnvsim/manage.py", "runserver", "0.0.0.0:8000"]