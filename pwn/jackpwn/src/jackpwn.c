#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define MISE 2

const char roulette[] = "xRNRNRNRNRNNRNRNRNRRNRNRNRNRNNRNRNRNR";

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

int get_random_number() {
    return 1 + (random() % 36);
}

int main() {
    int bille;
    char gagne;
    char valide, rouge, noir, pair, impair;

    struct {
        char mise[32];
        int solde;
    } ctx;

    ctx.solde = 50;

    srand(time(NULL));

    while (ctx.solde > 0) {
        valide = rouge = noir = pair = impair = 0;
        gagne = 0;

        do {
            printf("Solde : %d\n", ctx.solde);
            printf("Votre mise : ");
            fflush(stdout);
            read_input(ctx.mise);

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
        } while (!valide);

        bille = get_random_number();
        printf("La bille s'est stoppée sur la case %d (%c)\n", bille, roulette[bille]);

        if (rouge && roulette[bille] == 'R') {
            gagne = 1;
        } else if (noir && roulette[bille] == 'N') {
            gagne = 1;
        } else if (pair && ((bille % 2) == 0)) {
            puts("pair");
            gagne = 1;
        } else if (impair && ((bille % 2) == 1)) {
            puts("impair");
            gagne = 1;
        } else {
            gagne = 0;
        }

        if (gagne) {
            puts("Gagné");
            ctx.solde += MISE;
        } else {
            puts("Perdu");
            ctx.solde -= MISE;
        }

        if (ctx.solde == 0x1337) {
            char *flag = getenv("FLAG");
            if (flag == NULL) {
                puts("fake_flag");
            } else {
                puts(flag);
            }
            return 0;
        }
    }
}
