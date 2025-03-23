FROM ubuntu:20.04 AS builder
# ubuntu:20.04 is needed to get a libc 2.31 without heap pointer mangling

RUN apt-get update && apt-get install -y gcc patchelf

COPY binary_cooker.c /
RUN gcc -g /binary_cooker.c -o /binary_cooker && \
    patchelf --set-interpreter ld-2.31.so /binary_cooker && \
    patchelf --set-rpath . /binary_cooker && \
    patchelf --replace-needed libc.so.6 libc-2.31.so /binary_cooker

FROM debian:bookworm-slim

ENV TIMEZONE=Europe/Paris

#RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    #apt-get update && apt-get install -y --no-install-recommends python3-pip

RUN useradd -u 666 --home=/challenge -U challenge

COPY --chown=root:root --chmod=0555 --from=builder /binary_cooker /challenge/challenge
COPY --chown=root:root --chmod=0555 ld-2.31.so /challenge/
COPY --chown=root:root --chmod=0555 libc-2.31.so /challenge/
COPY --chown=root:root --chmod=0444 flag.txt /challenge/flag.txt

USER challenge
WORKDIR /challenge/

# needed to be able to reach the challenge from outside of the container
ENV CHALL_IS_IN_CONTAINER=1
ENTRYPOINT ["/challenge/challenge"]
