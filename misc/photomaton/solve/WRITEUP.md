# BreizhCTF 2025 | Write-up : Cheese ! [Misc]

Auteur : [skilo](https://skilo.sh)

La [transformation du cliché photomaton](https://fr.wikipedia.org/wiki/Transformation_du_clich%C3%A9_Photomaton) est une transformation d'image bijective. Lorsqu'on l'applique plusieurs fois de suite à une image, on revient toujours à la même image !

Pour résoudre ce challenge, il suffit donc de calculer la période et d'appliquer $\text{période} - 13$ fois la transformation à l'image d'output.

D'après Wikipedia, on calcule, pour une image de taille $2^k \times 2^l$, la période de cette manière :
$$\text{période} = \lcm(k, l)$$

Il ne nous reste donc plus qu'à implémenter la transformation (ou alors à utiliser une implémementation disponible sur internet) pour résoudre ce challenge !

Une implémentation de la solution complète de ce challenge est dispo dans le fichier `solve.py`.

