# Welcome Game - K.L.M

## Contrat
On a ici un contrat avec une grille :
```solidity
    constructor() {
        solved = false;
        initialGrid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ];
    }
```
Notre objectif est de passer la variable "solved" à TRUE. Pour ce faire, nous devons soumettre une solution au jeu.

## Solve
On remarque qu'il effectue plusieurs checks lorsque nous appelons la fonction "submitSolution()" après quelques vérifications on comprend que c'est un sudoku. On sort donc notre meilleur solver en ligne et on récupère la solution.

```solidity
[
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9]
    ]
```
On appele ensuite la fonction après avoir exporté nos variable d'environnement ($TARGET = contrat challenge, $PK = private-key, $RPC = url du RPC):

```bash
~ cast send $TARGET "submitSolution(uint8[9][9])" '[[5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],[8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],[9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]]' -r $RPC --private-key $PK

~ cast call $TARGET "solved()(bool)" -r $RPC
true
```

Win !
On récupère ensuite notre flag sur la plateforme.
