# Blind Guy - K.L.M

## Contrat
Bonne nouvelle (non), lorsque l'on lance le challenge et qu'on arrive sur la page, nous remarquons qu'aucun contrat nous est fourni...

Il ne nous reste plus qu'à sortir notre meilleur atout A.K.A le reverse.

Pour reverse un contrat, il nous faut son bytecode, on va donc le récupérer :
```bash
# $TAR = adresse du contrat cible, $RPC = URL du RPC
cast code $TAR -r $RPC

0x608060405234801561000f575f5ffd5b5060043610610055575f3560e01c806364d98f6e14610059578063799320bb14610077578063ec7eba0514610095578063ed74d933146100c5578063fe27c0f6146100e1575b5f5ffd5b6100616100ff565b60405161006e9190610446565b60405180910390f35b61007f610113565b60405161008c9190610446565b60405180910390f35b6100af60048036038101906100aa91906104bd565b610124565b6040516100bc9190610503565b60405180910390f35b6100df60048036038101906100da9190610546565b610141565b005b6100e96103c4565b6040516100f69190610503565b60405180910390f35b5f5f5f9054906101000a900460ff16905090565b5f5f9054906101000a900460ff1681565b6001602052805f5260405f205f915054906101000a900460ff1681565b5f5f9054906101000a900460ff161561018f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610186906105cb565b60405180910390fd5b600a60ff1660015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f9054906101000a900460ff1660ff1610610221576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161021890610633565b60405180910390fd5b5f6102753360015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f9054906101000a900460ff166103c9565b90508015158215150361036a5760015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f81819054906101000a900460ff16809291906102db9061067e565b91906101000a81548160ff021916908360ff16021790555050600a60ff1660015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f9054906101000a900460ff1660ff16036103655760015f5f6101000a81548160ff0219169083151502179055505b6103c0565b5f60015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f6101000a81548160ff021916908360ff1602179055505b5050565b600a81565b5f5f8383306040516020016103e09392919061071f565b6040516020818303038152906040528051906020012090505f6002825f6020811061040e5761040d61075b565b5b1a60f81b60f81c61041f91906107b5565b60ff161491505092915050565b5f8115159050919050565b6104408161042c565b82525050565b5f6020820190506104595f830184610437565b92915050565b5f5ffd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61048c82610463565b9050919050565b61049c81610482565b81146104a6575f5ffd5b50565b5f813590506104b781610493565b92915050565b5f602082840312156104d2576104d161045f565b5b5f6104df848285016104a9565b91505092915050565b5f60ff82169050919050565b6104fd816104e8565b82525050565b5f6020820190506105165f8301846104f4565b92915050565b6105258161042c565b811461052f575f5ffd5b50565b5f813590506105408161051c565b92915050565b5f6020828403121561055b5761055a61045f565b5b5f61056884828501610532565b91505092915050565b5f82825260208201905092915050565b7f4368616c6c656e676520616c726561647920736f6c76656421000000000000005f82015250565b5f6105b5601983610571565b91506105c082610581565b602082019050919050565b5f6020820190508181035f8301526105e2816105a9565b9050919050565b7f596f75206861766520616c726561647920776f6e2100000000000000000000005f82015250565b5f61061d601583610571565b9150610628826105e9565b602082019050919050565b5f6020820190508181035f83015261064a81610611565b9050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f610688826104e8565b915060ff820361069b5761069a610651565b5b600182019050919050565b5f8160601b9050919050565b5f6106bc826106a6565b9050919050565b5f6106cd826106b2565b9050919050565b6106e56106e082610482565b6106c3565b82525050565b5f8160f81b9050919050565b5f610701826106eb565b9050919050565b610719610714826104e8565b6106f7565b82525050565b5f61072a82866106d4565b60148201915061073a8285610708565b60018201915061074a82846106d4565b601482019150819050949350505050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52603260045260245ffd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601260045260245ffd5b5f6107bf826104e8565b91506107ca836104e8565b9250826107da576107d9610788565b5b82820690509291505056fea264697066735822122053b44d351a34a3a7d641e2a86a1cf55fec17c764b9afb2693024d79310ef08d964736f6c634300081c0033
```

On se rend sur notre decompiler préféré, le mien est "Dedaub" : [Lien Ici](https://app.dedaub.com) et on lui donne gentillement notre bytecode afin d'y voir plus clair (bonne blague).

On obtient un output de ce genre :
```solidity
bool _solved; // STORAGE[0x0] bytes 0 to 0
mapping (address => uint8) owner; // STORAGE[0x1]

function fallback() public payable { 
    revert();
}

function isSolved() public payable { 
    return _solved;
}

function solved() public payable { 
    return _solved;
}

function 0xec7eba05(address varg0) public payable { 
    require(4 + (msg.data.length - 4) - 4 >= 32);
    return owner[varg0];
}

function 0xed74d933(bool varg0) public payable { 
    require(4 + (msg.data.length - 4) - 4 >= 32);
    require(!_solved, Error('Challenge already solved!'));
    require(owner[msg.sender] < uint8(10), Error('You have already won!'));
    require(0 < 32, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
    require(uint8(2), Panic(18)); // division by zero
    if (varg0 - (uint8(uint8((byte(keccak256(msg.sender, owner[msg.sender], address(this)), 0x0)) << 248 >> 248) % uint8(2)) == 0)) {
        owner[msg.sender] = 0;
    } else {
        require(owner[msg.sender] - uint8.max, Panic(17)); // arithmetic overflow or underflow
        owner[msg.sender] = owner[msg.sender] + 1;
        if (!(owner[msg.sender] - uint8(10))) {
            _solved = 1;
        }
    }
}

function 0xfe27c0f6() public payable { 
    return uint8(10);
}

function __function_selector__( function_selector) public payable { 
    MEM[64] = 128;
    require(!msg.value);
    if (msg.data.length >= 4) {
        if (0x64d98f6e == function_selector >> 224) {
            isSolved();
        } else if (0x799320bb == function_selector >> 224) {
            solved();
        } else if (0xec7eba05 == function_selector >> 224) {
            0xec7eba05();
        } else if (0xed74d933 == function_selector >> 224) {
            0xed74d933();
        } else if (0xfe27c0f6 == function_selector >> 224) {
            0xfe27c0f6();
        }
    }
    fallback();
}
```

Après un peu de lecture et de déduction, on rend ce code un peu plus propre et on identifie la partie qui nous intéresse :
```solidity
function 0xed74d933(bool varg0) public payable { //Fonction qui nous intéresse car elle manipule la variable "solved"

    require(!_solved, Error('Challenge already solved!')); // Si déjà solve, normal

    require(owner[msg.sender] < uint8(10), Error('You have already won!')); // Pareil

    if (varg0 - (uint8(keccak256(msg.sender, owner[msg.sender], address(this))) % uint8(2)) == 0) { // Si notre argument (bool donc 0 ou 1) moins le résultat de : uint8(keccak256(MonAddresse, owner[msg.sender], AdresseContrat)) modulo 2 == 0 est de 1, soit ma valeur est différente de celle calculée, alors on remet à 0 le mapping.
        owner[msg.sender] = 0;
    } 
    //
    else { //sinon, ajoute 1 au mapping
        owner[msg.sender] = owner[msg.sender] + 1;

        if (!(owner[msg.sender] - uint8(10))) { //si le mapping est = 10, alors solved = true et WIN WIN WIN
            _solved = 1;
        }
    }
}
```
Etant donné qu'on se base ici sur des variables qui ne changent pas SAUF le mapping `owner[msg.sender]`, on peut le faire de deux façons. Soit nous écrivons un contrat qui calcule automatiquement les conditions pour satisfaire à chaque appel de fonction les prérequis, soit nous le faisons à la main et dans ce cas, nous devons mémoriser le chemin au cas ou nous aurions un retour à 0.

Afin de faire un write-up propre, je vais créer un contrat qui va le faire automatiquement. (Disponible au fichier contracts/attack.sol)

## Solve

Une fois le contrat créé, on le déploie, et on appelle la fonction solve: \$ATK = adresse du contrat attack, \$TAR = adresse du contrat cible, \$PK = clé privée, \$RPC = URL du RPC

```bash
cast send $ATK "setTarget(address)" $TAR -r $RPC --private-key $PK
cast send $ATK "solve()" -r $RPC --private-key $PK
```

Win !
On récupère ensuite notre flag sur la plateforme.
