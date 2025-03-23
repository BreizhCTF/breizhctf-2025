/* BREIZHCTF 2025 - Morph - Pwn */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

void transform() {
    void *shellcode;
    ssize_t bytes_read;

    shellcode = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (shellcode == MAP_FAILED) {
        perror("mmapi fail.");
        exit(1);
    }

    printf("Métamorph attend son code... Transforme-le !\n");
    printf(">> ");
    
    bytes_read = read(0, shellcode, 0x50); // Limité à 80 octets
    
    if (bytes_read <= 0) {
        perror("read failed");
        exit(1);
    }

    // Morphing...
    unsigned char *sc = (unsigned char *)shellcode;
    for (int i = 0; i < 0x50; i++) {
        if (sc[i] == 0x62){
            perror("Métamorph n'aime pas les 'b'.");
            exit(1);
        }

        if (sc[i] == 0x5e){
            perror("Métamorph n'aime pas les pop rsi.");
            exit(1);
        }

        if (sc[i] == 0x31){
            perror("Métamorph n'aime pas les xor.");
            exit(1);
        }

        if (sc[i] == 0x50){
            perror("Métamorph n'aime pas les push rax.");
            exit(1);
        }

    }

    ((void (*)())shellcode)(); // Exécution du shellcode transformé
}

int main() {
    setbuf(stdout, NULL);
    puts("⠀⠀⠀⢠⡜⠛⠛⠿⣤⠀⠀⣤⡼⠿⠿⢧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀");
    puts("⠀⣀⡶⠎⠁⠀⠀⠀⠉⠶⠶⠉⠁⠀⠀⠈⠹⢆⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀");
    puts("⣀⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠶⠶⠶⠶⣆⡀⠀⠀⠀⠀");
    puts("⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢣⡄⠀⠀⠀");
    puts("⠛⣧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀");
    puts("⠀⠛⣧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠀⠀⠀⠀⢠⡼⠃⠀⠀");
    puts("⠀⠀⠿⢇⡀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠶⢆⣀⣀⣀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀");
    puts("⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀");
    puts("⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀");
    puts("⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢣⣤");
    puts("⠀⣶⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿");
    puts("⠀⠿⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⢀⣀⣸⠿");
    puts("⠀⠀⠙⢳⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡞⠛⠛⠛⠛⠛⠛⣶⣶⣶⣶⡞⠛⠃⠀");
    puts("\n");
    puts("------------------------------");
    puts("\n");
    puts("Méta méta métamorph.");

    transform();
    return 0;
}
