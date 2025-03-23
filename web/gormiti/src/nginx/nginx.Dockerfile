FROM nginxinc/nginx-unprivileged

COPY ./default.conf /etc/nginx/conf.d/