Fonction de génération aléatoire inspiré de middle-square https://en.m.wikipedia.org/wiki/Middle-square_method

Cette méthode ne permet pas de créer des chaines aléatoires de période très longue.

A partir d'une seed fixée, on va mélanger le QR code avec l'élément x généré à partir de la seed. Indice entre 2\*\*12 et 2\*\*13 => possible de BF pour retrouver la vraie seed utilisée pour mélanger. 
