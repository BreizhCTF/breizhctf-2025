FROM node:23-bookworm-slim

RUN adduser bot

RUN apt update && apt install -y --no-install-recommends libnss3 libgtk-3-0 libasound2 libgbm1 tini && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN chown bot:bot /app

USER bot

RUN npm install express@4.21.2 puppeteer@24.2.0 && rm -rf ~/.npm

COPY ./src .

ENTRYPOINT ["tini", "--"]

CMD ["node", "bot.js"]