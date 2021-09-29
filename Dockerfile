FROM ubuntu:20.04

COPY ./requirements.txt /

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update -y \
    # python3 with pip
    && apt-get install -y python3-pip \
    # pyvirtualdiplay requires xvfb (which does not work on MacOS), checkout https://github.com/ponty/pyvirtualdisplay/tree/2.2
    && apt-get install -y xvfb xserver-xephyr tigervnc-standalone-server xfonts-base \
    # installing google chrome
    && apt-get install -y wget \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    # Remove mirrors making minimal image
    && rm -rf /var/lib/apt/lists/* \ 
    # install dependencies
    && python3 -m pip install -r requirements.txt

EXPOSE 5000

COPY . .

ENTRYPOINT ["python3", "main.py", "--url", "http://www.aastocks.com/tc/stocks/quote/dynamic-chart.aspx?index=221000.FT"]