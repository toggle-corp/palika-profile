FROM ubuntu:18.04

MAINTAINER togglecorp info@togglecorp.com

ENV DEBIAN_FRONTEND=noninteractive
ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update -y \
    && apt-get install -y \
        libgirepository1.0-dev \
        gcc \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        libcairo2-dev \
        pkg-config \
        gir1.2-gtk-3.0 \
        gir1.2-rsvg-2.0 \
        curl \
        unzip \
        vim \
        wget \
        git \
        software-properties-common \
    # Install QGIS
    && wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import \
    && chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg \
    && add-apt-repository "deb https://qgis.org/debian bionic main" \
    && apt-get update -y \
    && apt-get install -y qgis python3-qgis \
    # Install required fonts
    && curl -L https://github.com/google/roboto/releases/download/v2.138/roboto-android.zip -o /tmp/font.zip \
    && unzip -o /tmp/font.zip -d /root/.fonts/ \
    && curl -L https://noto-website-2.storage.googleapis.com/pkgs/NotoSansDevanagari-hinted.zip -o /tmp/font1.zip \
    && unzip -o /tmp/font1.zip -d /root/.fonts/ \
    && curl -L https://noto-website-2.storage.googleapis.com/pkgs/NotoSans-hinted.zip -o /tmp/font2.zip \
    && unzip -o /tmp/font2.zip -d /root/.fonts/ \
    && fc-cache --force --verbose \
    # Remove apt cache to make the image smaller
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt ./requirements.txt
RUN echo 'alias python=python3\nalias pip=pip3' >> ~/.bashrc \
    && pip3 install -r requirements.txt

COPY . /code/

# Need to reinstall hrrpmaps and drafter for each build
RUN pip3 install --src /dep/ -e "git+https://github.com/eoglethorpe/hrrp-maps@master#egg=hrrpmaps" \
    && pip3 install --src /dep/ -e "git+https://github.com/toggle-corp/drafter@develop#egg=drafter"
