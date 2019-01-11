FROM ubuntu:18.04

MAINTAINER togglecorp info@togglecorp.com

ENV DEBIAN_FRONTEND=noninteractive
ENV QT_QPA_PLATFORM=offscreen
ARG UBUNTU_GIS_REPO='https://qgis.org/debian'

RUN apt-get update -y ; \
    apt-get install -y \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        curl \
        unzip \
        vim \
        wget \
        git \
        software-properties-common && \
    echo "deb ${UBUNTU_GIS_REPO} bionic main" >> /etc/apt/sources.list && \
    echo "deb-src ${UBUNTU_GIS_REPO} bionic main" >> /etc/apt/sources.list && \
    wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import && \
    gpg --fingerprint CAEB3DC3BDF7FB45 && \
    gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add - && \
    apt-get update -y ; \
    apt-get install -y \
        python3-gi \
        python3-gi-cairo \
        gir1.2-gtk-3.0 \
        gir1.2-rsvg-2.0 \
        qgis-server \
        python-qgis

WORKDIR /code

RUN curl -L https://github.com/google/roboto/releases/download/v2.138/roboto-android.zip -o /tmp/font.zip && \
    unzip -o /tmp/font.zip -d /root/.fonts/ && \
    curl -L https://noto-website-2.storage.googleapis.com/pkgs/NotoSansDevanagari-hinted.zip -o /tmp/font1.zip && \
    unzip -o /tmp/font1.zip -d /root/.fonts/ && \
    curl -L https://noto-website-2.storage.googleapis.com/pkgs/NotoSans-hinted.zip -o /tmp/font2.zip && \
    unzip -o /tmp/font2.zip -d /root/.fonts/ && \
    fc-cache --force --verbose

COPY ./requirements.txt /code/requirements.txt

RUN  pip3 install -r requirements.txt

COPY . /code/
