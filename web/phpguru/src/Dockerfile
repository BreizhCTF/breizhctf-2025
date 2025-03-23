FROM php:8.3-apache

RUN apt update && apt install -y python3

COPY game/ /var/www/html/

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY flag.txt /flag.txt

ENTRYPOINT ["/entrypoint.sh"]