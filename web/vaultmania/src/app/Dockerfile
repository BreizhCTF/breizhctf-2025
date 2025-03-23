ARG REGISTRY=registry-bzh.alfred.cafe

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/uwsgi

COPY --chown=root:root ./requirements.txt requirements.txt

RUN pip install -r requirements.txt --break-system-packages

COPY --chown=root:root --chmod=777 ./src .