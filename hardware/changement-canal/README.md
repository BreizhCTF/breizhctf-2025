# Changement de canal

Catégorie : Hardware

Difficulté : Moyen

Auteur : ribt

## Description publique

Un collègue a découvert comment fonctionnait le [dispositif CTCSS](https://fr.wikipedia.org/wiki/CTCSS) qui permet à plusieurs utilisateurs de partager une même fréquence radio sans s'interférer, en créant artificiellement des canaux. Il a décidé d'utiliser ce mécanisme pour communiquer discrètement avec ses amis. Il a créé un dispositif qui joue une musique en changeant de canal toutes les trois secondes. Une émission sur le canal 1 désigne la transmission la lettre `A`, le canal 2 pour la lettre `B`, etc. jusqu'au canal 26 pour la lettre `Z`. Une pause sans canal entre deux lettres correspond à un espace (représenté par un `_` dans le flag).

Vous avez allumé votre talkie-walkie et entendu la musique envoyée par son dispositif. Retrouvez le message caché.

Le flag est en majuscules au format `BZHCTF{MESSAGE_EN_PLUSIEURS_MOTS}`.

## Description interne

Utilisation de changement de canaux CTCSS pour cacher des données dans une musique.

## Flag

`BZHCTF{LES_CANAUX_CTCSS_NE_SONT_PAS_CONFIDENTIELS_DU_TOUT}`