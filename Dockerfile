FROM ubuntu:14.04
LABEL MAINTAINER "Abdelrahman Hosny <abdelrahman.hosny@hotmail.com>"

# install python
RUN apt-get update && \
apt-get install -y python python-pip libgsl0ldbl && \
apt-get clean && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV PYTHONUNBUFFERED 1

# install dependencies for Wessim
RUN apt-get update && \
    apt-get install -y build-essential python-pip wget bedtools
RUN apt-get install -y zlib1g-dev libcurl4-openssl-dev python-dev libxml2-dev libxslt-dev
RUN apt-get install -y libz-dev libbz2-dev liblzma-dev
RUN wget https://github.com/samtools/htslib/releases/download/1.8/htslib-1.8.tar.bz2 -O htslib.tar.bz2 && \
    tar -xjvf htslib.tar.bz2 && \
    cd htslib-1.8 && \
    make && \
    make install
RUN pip install pysam && \
    pip install numpy

# add external software libraries
ADD easyscnvsim_lib /easyscnvsim_lib
WORKDIR /easyscnvsim_lib/pblat
RUN make

# add web app
RUN mkdir /easyscnvsim
WORKDIR /easyscnvsim
ADD requirements.txt /easyscnvsim/
RUN pip install -r requirements.txt

ADD easyscnvsim /easyscnvsim/easyscnvsim
ADD webapp /easyscnvsim/webapp
ADD manage.py /easyscnvsim/manage.py

RUN python manage.py migrate


EXPOSE 8000
ENTRYPOINT ["python", "/easyscnvsim/manage.py", "runserver", "0.0.0.0:8000"]