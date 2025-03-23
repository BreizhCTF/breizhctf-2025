ARG REGISTRY=registry-bzh.alfred.cafe

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/uwsgi

WORKDIR /challenge

RUN pip3 install flask requests --break-system-packages

# COPY DES FILES
RUN mkdir /challenge/static
RUN mkdir /challenge/templates

COPY ./static/ /challenge/static/
COPY ./templates/ /challenge/templates/
COPY ./server.py /challenge/
COPY ./crypto_data.json /challenge/

# NOTES.TXT
RUN mkdir /home/crepesmaster
COPY ./priv_key/notes.txt /home/crepesmaster/

