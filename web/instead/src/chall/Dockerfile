FROM node:18.16.0-bookworm-slim

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV XDG_CONFIG_HOME=/tmp
ENV XDG_CACHE_HOME=/tmp
ENV NODE_ENV=production

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends chromium curl && \
    rm -rf /var/lib/apt/lists/* && \
    useradd instead && \
    chown instead:instead /app

COPY --chown=instead:instead . .
RUN mkdir -p uploads/cv/ && chown -R instead:instead uploads

RUN corepack enable && \
    yarn plugin import workspace-tools && \
    yarn workspaces focus --production && \
    rm -rf .yarn

USER instead

EXPOSE 5000

CMD ["node", "index.js"]
