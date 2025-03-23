# BreizhCTF 2025 | Write-up : As-tu de bons yeux ? [Crypto]

Auteur : [skilo](https://skilo.sh)

## Quelques notations

- $[\beta]$ : l'ensemble $\{-\beta, -\beta+1, \ldots, 0, \ldots, \beta-1, \beta\}$.
- $\mathbb{Z}_{n}$ : l'anneau des entiers modulo $n$, aussi noté $\mathbb{Z}/n\mathbb{Z}$.

---

Il est évidemment impossible — du moins à l'heure actuelle — de casser le problème (D-)MLWE lorsque celui-ci utilise le paramétrage de niveaux 5 de ML-DSA ; il est donc nécessaire de trouver une erreur d'implémentation.

Nous pouvons remarquer que, dans le fichier `parameters.sage` le polynôme par lequel est quotienté l'anneau $\mathbb{Z}_q[X]$ est $X^{256} - 1$ au lieu de $X^{256} + 1$. Ce dernier est factorisable dans $\mathbb{Z}$. En effet : 

$$X^{256} - 1 = {\left(X^{128} + 1\right)} {\left(X^{64} + 1\right)} {\left(X^{32} + 1\right)} {\left(X^{16} + 1\right)} {\left(X^{8} + 1\right)} {\left(X^{4} + 1\right)} {\left(X^{2} + 1\right)} {\left(X + 1\right)} {\left(X - 1\right)}$$

Posons $f = X^{256} - 1$ et $g = X - 1$, nous avons un morphisme d'anneau allant de $\mathbb{Z}_q[X]/f$ vers $\mathbb{Z}_q[X]/g$ qui map les éléments $a = \sum_{i = 0}^{256} a_iX^i \in \mathbb{Z}_q[X]$ vers $a' = \sum_{i = 0}^{256} a_i \in \mathbb{Z}_q[X]$ (Bref. C'est une évaluation en $X = 1$).

Il map donc les éléments vers $\mathbb{Z}_q$ (en effet, $\mathbb{Z}_q[X]/g$ est isomorphique à $\mathbb{Z}_q$), ce qui est cool avec ce morphisme c'est qu'il "préserve" à peu près la taille des coefficients, c'est-à-dire que, si un élément de $\mathbb{Z}_q[X]/f$ a des coefficients dans $[\beta]$, alors, en sortie du morphisme il deviendra un élément de $[256\beta]$. Comme $256 \ll q$, l'élément reste "petit".

Si nous avons une instance du D-MLWE : $\mathbf{t} = \mathbf{A}\mathbf{s} + \mathbf{e}$, où $\mathbf{t}$, $\mathbf{s}$ et $\mathbf{e}$ sont des vecteurs de $\mathbb{Z}_q[X]/f$ et où $\mathbf{A}$ est une matrice de ce même ensemble. Nous pouvons appliquer ce morphisme à chacun de ces éléments et nous retrouver ainsi avec un D-MLWE $t' = A's' + e'$ de très petit paramétrage et dans $Z_q$ (se résout très efficacement avec `LLL()`/`BKZ()`).

En effet, si nous trouvons un $s'$ et un $e'$ avec des coefficients dans $[256\beta]$, alors, il s'agit d'une instance du MLWE ; sinon, non. Grâce à cette stratégie, nous pouvons résoudre le challenge ! Une implémentation complète de cette solution est disponible dans le fichier `solve.sage`.

Pour plus de ressources sur ce sujet, la section 4.5 du paper [Basic Lattice Cryptography - The concepts behind Kyber (ML-KEM) and Dilithium (ML-DSA)](https://eprint.iacr.org/2024/1287.pdf) de Vadim Lyubashevsky explique très bien cette attaque.

