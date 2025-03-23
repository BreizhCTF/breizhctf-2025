# Changement de canal - SOLUTION

## Énoncé

>  Un collègue a découvert comment fonctionnait le [dispositif CTCSS](https://fr.wikipedia.org/wiki/CTCSS) qui permet à plusieurs utilisateurs de partager une même fréquence radio sans s'interférer, en créant artificiellement des canaux. Il a décidé d'utiliser ce mécanisme pour communiquer discrètement avec ses amis. Il a créé un dispositif qui joue une musique en changeant de canal toutes les trois secondes. Une émission sur le canal 1 désigne la transmission la lettre `A`, le canal 2 pour la lettre `B`, etc. jusqu'au canal 26 pour la lettre `Z`. Une pause sans canal entre deux lettres correspond à un espace (représenté par un `_` dans le flag).
>
>     Vous avez allumé votre talkie-walkie et entendu la musique envoyée par son dispositif. Retrouvez le message caché.
>
>     Le flag est en majuscules au format `BZHCTF{MESSAGE_EN_PLUSIEURS_MOTS}`.

## Résolution

Sur l'article lié dans l'énoncé on peut retrouver les fréquences des canaux.

On peut confirmer ces fréquences avec un autre site : http://pmr446.free.fr/index_codage_ctcss.htm

On commence par convertir `record.mp3` en wav (avec Audacity par exemple), ça sera plus facile à ouvrir en Python.

On donne un prompt à ChatGPT tel que *Fais un programme Python pour faire la FFT d'un signal dans un fichier wav et indiquer la fréquence (entre 67 Hz et 163 Hz) avec la plus grande amplitude pour chaque tranche de 3s*. En adaptant un peu on obtient le programme [solve.py](solve.py).

En lançant le programme on obtient :

```
_LES_CANAUX_CTCSS_NE_SONT_PAS_CONFIDENTIELS_DU_TOUT______O______
```

Le flag est `BZHCTF{LES_CANAUX_CTCSS_NE_SONT_PAS_CONFIDENTIELS_DU_TOUT}`.