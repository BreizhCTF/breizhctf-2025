FROM python:3.10-slim

RUN adduser --disabled-password appuser

WORKDIR /app

RUN pip install --no-cache-dir cryptography \
    && rm -rf /root/.cache /var/cache/apk/*

COPY ./app /app

USER appuser

EXPOSE 4444

CMD ["python3", "/app/UEFInfected_server.py"]
