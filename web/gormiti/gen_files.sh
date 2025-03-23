#!/bin/sh
cp -r src/* files

cd files
echo "FROM golang:1.24.0-bullseye AS builder
WORKDIR /app
COPY go.mod go.sum .
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -v -o backend .

FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app .
EXPOSE 8080
CMD [\"./backend\"]" > ./app/Dockerfile

zip -rm GORMiti.zip app nginx compose.yml