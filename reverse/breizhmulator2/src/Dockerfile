FROM python:3.10-slim

# Créer un utilisateur non privilégié
RUN adduser --disabled-password appuser

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY ./app /app

# Changer la propriété des fichiers copiés pour l'utilisateur appuser
RUN chown -R appuser:appuser /app

# Rendre l'exécutable /app/vm
RUN chmod u+x /app/vm

# Passer à l'utilisateur non privilégié
USER appuser

# Exposer le port 5000
EXPOSE 5000

# Exécuter le serveur
CMD ["python3", "/app/server.py"]
