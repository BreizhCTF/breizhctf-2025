ARG REGISTRY=registry-bzh.alfred.cafe

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/uwsgi

COPY src /challenge
COPY requirements.txt /challenge

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
ENV FLAG=BZHCTF{encore_et_toujours_de_la_faute_du_stagiaire_350cd55e8bf628ea}
