FROM ubuntu:24.10

ENV TIMEZONE Europe/Paris

# Mise à jour et installation des paquets nécessaires
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 python3-pip socat qemu-system-riscv64 mtools && \
    rm -rf /var/lib/apt/lists/*

# Création d'un utilisateur non privilégié
RUN useradd -m -d /app -s /bin/bash user && \
    mkdir -p /app/upload && \
    chown user:user /app/upload && chmod 700 /app/upload    

WORKDIR /app

# Copie des fichiers
COPY --chown=user:user --chmod=0755 src/server.py /app/server.py
COPY --chown=user:user --chmod=0644 src/barebox-dt-2nd.img /app/barebox-dt-2nd.img
COPY --chown=user:user --chmod=0644 src/flag.img /app/flag.img

# Exposition du port
EXPOSE 1337

# Exécution sous l'utilisateur non root
USER user

# Lancement du service via socat
ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork,max-children=10", "EXEC:/usr/bin/python3 /app/server.py,stderr,pty,cfmakeraw,echo=0"]

