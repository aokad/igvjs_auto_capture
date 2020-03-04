FROM ubuntu:18.04
MAINTAINER aokad <aokada@ncc.go.jp>

WORKDIR /work
RUN apt-get update -y && \
    apt-get install -y xvfb firefox wget python3-pip git && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar -zxvf geckodriver-v0.26.0-linux64.tar.gz && \
    rm -f geckodriver-v0.26.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod 755 /usr/local/bin/geckodriver && \
    pip3 install selenium

RUN pip3 install boto3 && \
    git clone https://github.com/aokad/igvjs_auto_capture.git
