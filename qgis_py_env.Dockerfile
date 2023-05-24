FROM ubuntu:22.10


LABEL maintainer="Vladimir Morozov <raulett@gmail.com>"



ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev python3-virtualenv git-core wget unzip gnupg software-properties-common

RUN wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg && \
touch /etc/apt/sources.list.d/qgis.sources && \
printf "Types: deb deb-src\nURIs: https://qgis.org/debian-ltr\nSuites: kinetic\n\
Architectures: amd64\nComponents: main\nSigned-By: /etc/apt/keyrings/qgis-archive-keyring.gpg" > /etc/apt/sources.list.d/qgis.sources
ENV TZ="UTC"
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
RUN apt-get install -y qgis python-qgis qgis-plugin-grass pyqt5-dev-tools

RUN pip3 install --upgrade pip
RUN pip3 install numpy scipy pandas geopandas

RUN mkdir /rousettus
ENV HOME=/rousettus
ENV SHELL=/bin/bash
ENV PYTHONPATH=/usr/share/qgis/python
ENV LD_LIBRARY_PATH=/usr/share/qgis/python
#VOLUME /rousettus
WORKDIR /rousettus

#CMD ["/bin/bash"]