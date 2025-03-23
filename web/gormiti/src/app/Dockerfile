FROM golang:1.24.0-bullseye AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -v -o backend .

FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV FLAG=BZHCTF{G0rM1t1_1s_4m4z1ng_3v3n_w1th_h2c_smuggl1ng_4nd_sQL1}
COPY --from=builder /app .
EXPOSE 8080
CMD ["./backend"]