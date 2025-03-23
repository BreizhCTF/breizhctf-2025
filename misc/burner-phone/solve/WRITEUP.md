# Writeup

En essayant les numéros de téléphone sur les différents champs, on se rend compte que le "Crack de mot de passe" nous indique le password "Ashley" pour les 3 numéros fournis.

Ces mêmes numéros semblent appartenir à la société "BurnerBZH" *(d'après le formulaire "Société téléphonique")*, dont les blocs de numéros sont compris dans [0733890000:0733899999] *(d'après le formulaire "Information sur la société téléphonique")*.

Un petit bruteforce du formulaire "Crack de mot de passe" sur les 10000 numéros de la société [à l'aide d'un script](solve.py) nous permet de récupérer différents mots de passe, dont 4 occurences du mot de passe "Ashley": 

- 0733891214
- 0733891373
- 0733896724
- 0733896810

Le numéro manquant est donc `0733891373`, ce qui nous donne le flag `BZHCTF{0733891373}`.