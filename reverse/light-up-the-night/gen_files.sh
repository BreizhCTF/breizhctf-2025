#!/bin/bash
# On supprime les fichiers
sudo rm -rf ./files/light_up_the_night_game.zip
# On build l'image docker qui sert à compiler le binaire
sudo docker build -t light_up_the_night -f src/Dockerfile.build src
# On lance un conteneur temporaire
sudo docker run -d --name light_up_the_night light_up_the_night:latest
# On extrait le binaire pour le copier dans files
sudo docker cp light_up_the_night:/dist/game ./files/
# On supprime le conteneur
sudo docker rm light_up_the_night
# On suprime l'image docker
sudo docker rmi light_up_the_night
# On zip le dossier game
cd files
zip -r light_up_the_night_game.zip game
sudo rm -rf game