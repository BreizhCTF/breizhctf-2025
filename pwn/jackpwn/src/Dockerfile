ARG REGISTRY=registry-bzh.alfred.cafe

# Build stage
FROM debian:bookworm AS builder

RUN apt-get update && apt-get install -y build-essential

COPY jackpwn.c /
RUN gcc -g /jackpwn.c -o /jackpwn


# Final stage
FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

COPY --chown=root:root --chmod=0555 --from=builder /jackpwn /challenge/challenge

USER challenge
WORKDIR /challenge/

ENV FLAG=BZHCTF{70u7_p0ur_14_p4\$\$10n_1e2f97a55353bcab}
