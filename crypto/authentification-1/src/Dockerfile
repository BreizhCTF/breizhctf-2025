ARG REGISTRY=registry-bzh.alfred.cafe

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/uwsgi

COPY src /challenge
COPY requirements.txt /challenge

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
ENV FLAG=BZHCTF{ne_jamais_re-utiliser_le_nonce_e1d6ce70d3d1018c}

