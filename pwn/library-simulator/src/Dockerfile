ARG REGISTRY=registry-bzh.alfred.cafe

# Build stage
FROM debian:bookworm AS builder

ARG CHALL_NAME=library_simulator 

RUN apt-get update && apt-get install -y build-essential patchelf

COPY ${CHALL_NAME}.c /
RUN gcc -fno-stack-protector -no-pie "/${CHALL_NAME}.c" -o "/${CHALL_NAME}" && \
    strip "/${CHALL_NAME}" && \
    patchelf --set-interpreter ld-linux-x86-64.so.2 "/${CHALL_NAME}" && \
    patchelf --set-rpath . "/${CHALL_NAME}"

# Final stage
FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

COPY --chown=root:root --chmod=0555 library_simulator /challenge/challenge
COPY --chown=root:root --chmod=0555 libc.so.6 /challenge/
COPY --chown=root:root --chmod=0555 ld-linux-x86-64.so.2 /challenge/
COPY --chown=root:root --chmod=0444 flag.txt /challenge/


USER challenge
WORKDIR /challenge/
