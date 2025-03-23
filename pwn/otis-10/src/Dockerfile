ARG REGISTRY=registry-bzh.alfred.cafe

# Build stage
FROM debian:bookworm AS builder

RUN apt-get update && apt-get install -y build-essential libbsd-dev

COPY otis_10.c /
RUN gcc -g /otis_10.c -o /otis_10 -lbsd


# Final stage

FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

USER root

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends libbsd-dev cowsay

USER challenge

COPY --chown=root:root --chmod=0555 --from=builder /otis_10 /challenge/challenge
COPY --chown=root:root --chmod=0444 flag.txt /challenge/flag.txt
