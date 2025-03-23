#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char msg[32];
    char name[64];
} creature_t;


creature_t *new_creature() {
    creature_t *creature = malloc(sizeof(*creature));

    // you may need to install cowsay for this to work
    FILE *p = popen("ls /usr/share/cowsay/cows/ | shuf -n1", "r");
    fgets(creature->name, sizeof(creature->name), p);
    pclose(p);

    return creature;
}

creature_t *new_cow() {
    creature_t *cow = malloc(sizeof(*cow));
    strlcpy(cow->name, "default", sizeof(cow->name));
    return cow;
}

void roaaar(creature_t *creature) {
    // you may need to install cowsay for this to work
    char cmd[256] = "echo 'Roarrr !' | /usr/games/cowsay -f ";
    strlcat(cmd, creature->name, sizeof(cmd));
    system(cmd);
}

void moo(creature_t *cow) {
    char *msg = malloc(96);

    printf("Message : ");
    fflush(stdout);
    fgets(msg, 96, stdin);


    FILE *p = popen("/usr/games/cowsay", "w");
    fwrite(msg, 1, strlen(msg), p);
    pclose(p);
}

void help() {
    puts("=== Otis 10 ===");
    puts("n : Nouvelle créature");
    puts("v : Se retransformer en vache");
    puts("r : Roaaar !");
    puts("m : Meuh !");
    puts("q : Quitter");
    printf("> ");
    fflush(stdout);
}


int main() {
    creature_t *cow = new_cow();
    creature_t *creature = NULL;

    char choice;
    char quit = 0;

    while (!quit) {
        help();

        char choice = getchar();
        while (getchar() != '\n') {}

        switch (choice) {
            case 'n':
                creature = new_creature();
                printf("Vous vous transformez en %s\n", creature->name);
                break;
            case 'v':
                free(creature);
                break;
            case 'r':
                if (creature != NULL) {
                    roaaar(creature);
                } else {
                    puts("Vous êtes une vache");
                }
                break;
            case 'm':
                moo(cow);
                break;
            case 'q':
                quit = 1;
                break;
            default:
                break;
        }
    }
}
