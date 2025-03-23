#include <stdlib.h>
#include <stdio.h>

int main() {
    char line[1024];

    printf("What is your name : ");
    fflush(stdout);

    scanf("%[^\n]", &line);
    fgetc(stdin);

    printf("Hello %s\n", line);

    return 0;
}
