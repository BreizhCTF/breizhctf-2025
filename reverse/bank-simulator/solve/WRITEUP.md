# Write-up : Bank-Simulator

*Ce challenge a été réalisé dans l'objectif de gagner une bière :*
> "Si vous me calez un chall de Cobol, je paie une biere" -- Zeecka


## Analyse initiale du binaire

Nous commençons par examiner le type de fichier fourni avec la commande `file` :

```sh
$ file bank-simulator

bank-simulator: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e54bba1560a88b8c9e17322fd9e0acf87636e741, for GNU/Linux 3.2.0, stripped
```

Le fichier est un binaire ELF 64 bits pour Linux, lié dynamiquement et **strippé**, ce qui signifie que les symboles de débogage ont été supprimés.

## Exécution du programme

Lancer l'exécutable affiche une interface simulant une procédure bancaire kafkaïenne :

```text
./bank-simulator
[BANK-SIMULATOR]
Bienvenue dans le simulateur bancaire ultime !

Voici les etapes :
1. Rendez-vous en physique (9h45-10h12 le mardi).
2. Completez le dossier (bonne chance pour
   comprendre les formulaires).
3. Retournez voir votre conseiller
   (si vous le retrouvez).
4. Ce n'etait pas le bon dossier,
   mais on vous l'avait dit, non ? Recommencez
5. Payez les frais de dossier (x2).
6. Une lettre devrait arriver d'ici 1-2 ans
   (ou pas).
7. Ouvrez-la, un code vous est peut-etre donne
   (si la poste ne l'a pas egare).
8. Saisissez le code ci-dessous pour acceder a
   l'ultime verite.

SAISIR LE CODE >
```

Le programme attend une entrée utilisateur, qui semble être un code secret. On a pas 2 ans devant nous à attendre le code, on va donc le trouver !

## Extraction des chaînes de caractères

L'outil `strings` nous permet de récupérer les chaînes de caractères présentes dans le binaire :

```sh
strings bank-simulator
```

Résultat pertinent :

```text
Bravo, vH
ous avezH
 triomphH
e de la H
bureaucrH
atie !  H
Mauvais H
code ! UH
n formulH
aire supH
plementaH
ire vousH
BZHCTF{CH
oB0l_4_3H
v3r}
```

Nous remarquons plusieurs éléments intéressants :
- Le message de succès « Bravo, vous avez triomphé de la bureaucratie ! »
- Le message d'échec « Mauvais code ! Un formulaire supplémentaire vous sera envoyé. »
- **Le flag : `BZHCTF{CoB0l_4_3v3r}`**, bien que coupé par des caractères `H` et des sauts de ligne inhabituels.

## Pourquoi ces coupures ?

*Explications chatGPT, car j'en sais rien, personne ne code en cobol -_-*

Le programme est écrit en **COBOL**, un langage conçu pour la gestion de données sur des systèmes anciens. En COBOL, les chaînes de caractères sont souvent stockées en **champs fixes**, ce qui peut expliquer les coupures visibles ici. L'utilisation d'un format de stockage spécifique, avec des longueurs de champ prédéfinies (par exemple 8 caractères), pourrait être responsable des espaces et des caractères supplémentaires (`H`).

## Conclusion

Une analyse statique du binaire avec `strings` permet directement de récupérer le flag sans avoir besoin de reverse complexe :).

> **Flag :** `BZHCTF{CoB0l_4_3v3r}`
