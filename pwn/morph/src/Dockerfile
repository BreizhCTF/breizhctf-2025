ARG REGISTRY=registry-bzh.alfred.cafe

FROM debian:bookworm AS builder

RUN apt-get update && apt-get install -y build-essential make

COPY metamorph.c /
COPY Makefile /

RUN make

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

COPY --chown=root:root --chmod=0755 --from=builder /metamorph /challenge/challenge
COPY --chown=root:root --chmod=0744 flag.txt /challenge/flag.txt
