ARG REGISTRY=registry-bzh.alfred.cafe

# Build stage
FROM debian:bookworm AS builder

RUN apt-get update && apt-get install -y build-essential

COPY hr_invalidation.cpp /

RUN g++ --std=c++23 -g /hr_invalidation.cpp -o /hr_invalidation

# Final stage
FROM ${REGISTRY}/breizh-ctf-2025/challenge/docker/tcp

COPY --chown=root:root --chmod=0755 --from=builder /hr_invalidation /challenge/challenge
ENV FLAG=BZHCTF{iterator_invalidation_are_cool_bugs_always_read_the_docs_0666e80a71a1513c}
