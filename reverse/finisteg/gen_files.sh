#!/bin/bash

# Fonction pour exécuter une commande avec gestion d'erreurs et check sudo
run_command() {
  "$@" || { echo "❌ Erreur lors de l'exécution de la commande: $@"; echo "👉 Vérifiez que vous avez les droits d'exécution Docker (sudo)."; exit 1; }
}

echo "🚀 Début de la compilation Docker..."

# Build de l'image Docker qui sert à compiler le binaire
echo "🔨 Construction de l'image Docker pour la compilation..."
run_command docker build -t finisteg -f ./src/Dockerfile.build ./src/
echo "✅ Image Docker construite avec succès."

echo ""
echo "🔄 Lancement d'un conteneur temporaire à partir de l'image..."

# Lancement du conteneur temporaire
run_command docker run --rm -d --name finisteg finisteg:latest
echo "✅ Conteneur lancé avec succès."

echo ""
echo "📂 Extraction des fichiers nécessaires depuis le conteneur..."

# Extraction du binaire et des fichiers nécessaires
run_command docker cp finisteg:/finisteg.apk ./files/
echo "✅ Fichiers extraits et copiés dans './files/'."

echo ""
echo "🛑 Arrêt du conteneur temporaire..."

# Arrêt du conteneur
run_command docker stop finisteg
echo "✅ Conteneur arrêté."

echo ""
echo "🧹 Suppression de l'image Docker pour libérer de l'espace..."

# Suppression de l'image Docker
run_command docker rmi finisteg
echo "✅ Image Docker supprimée."

echo ""
echo "🎉 Processus terminé avec succès ! Tous les fichiers sont prêts dans le dossier './files/'."
