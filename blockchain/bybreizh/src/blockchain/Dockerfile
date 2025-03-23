ARG REGISTRY=registry-bzh.alfred.cafe

# MARK: Build stage
FROM python:3 AS builder

SHELL ["/bin/bash", "-c"]

RUN wget -O - https://foundry.paradigm.xyz | bash && \
    ~/.foundry/bin/foundryup && \
    mkdir ~/blockchain && \
    cd ~/blockchain && \
    ~/.foundry/bin/forge install 'openzeppelin/openzeppelin-contracts@release-v5.0' --no-git && \
    ~/.foundry/bin/forge init --force --no-git && \
    rm -rf ./src/* && \
    rm -rf ./test/* && \
    rm -rf ./script/* && \
    rm -rf ./foundry.toml && ls -alh

COPY ./blockchain/ /root/blockchain/

RUN cd ~/blockchain && \
    ~/.foundry/bin/forge build && \
    ~/.foundry/bin/forge compile

# MARK: Final stage
FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/uwsgi

RUN sed -i 's/listen      80;/listen      9000;/' /etc/nginx/nginx.conf && \
    sed -i 's/listen       80;/listen      9000;/' /etc/nginx/conf.d/default.conf && \
    pip3 install eth_account requests web3 --break-system-packages && \
    apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/{cache,lib}/apt

USER challenge
RUN curl -sL https://foundry.paradigm.xyz | bash

RUN $HOME/.foundry/bin/foundryup
USER root

COPY ./app /challenge
COPY --from=builder --chown=challenge:challenge /root/blockchain /challenge/blockchain
