ARG REGISTRY=registry-bzh.alfred.cafe

# Dockerfile
FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

COPY requirements.txt .

USER root
RUN pip install -r requirements.txt --break-system-packages
USER challenge
COPY --chmod=700 --chown=challenge:challenge challenge.py /challenge/challenge

