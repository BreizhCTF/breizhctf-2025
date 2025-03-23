/* librairie
 *
 *
 * https://tenor.com/view/monster-librarian-library-gif-25590673
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_BOOKS 16

char *books[MAX_BOOKS] = {
    "La cabane magique",
    "La ferme des animaux",
};

int stock[MAX_BOOKS] = {
    2,
    1,
};

int get_book_idx(char *title) {
    for (int i = 0; i < MAX_BOOKS; i++) {
        if (books[i] == NULL) continue;

        if (!strcmp(title, books[i])) {
            return i;
        }
    }

    return -1;
}

int foo() {
    puts("hey");
    asm volatile("pop %rdi; ret;");
    return 0;
}

void borrow_book(char *title) {
    int idx = get_book_idx(title);

    if (idx == -1) {
        puts("Book not found");
        return;
    }

    if (stock[idx] <= 0) {
        puts("This book is no longer available");
        return;
    } else {
        stock[idx] -= 1;
    }
}

void return_book(char *title) {
    int idx = get_book_idx(title);

    if (idx == -1) {
        puts("This book does not exist");
        return;
    }

    stock[idx] += 1;
}

void print_stock() {
    puts("Stock:");
    for (int i = 0; i < MAX_BOOKS; i++) {
        if (books[i]) {
            printf("%s: %d\n", books[i], stock[i]);
        }
    }
}

void read_input(char *buf, size_t n) {
    char c;
    if (n == 0) return;

    while (n--) {
        c = getchar();
        if (c == '\n') {
            *buf++ = 0;
            break;
        }
        *(buf++) = c;
    }
}

int main() {
    char title[32];
    int size;
    char choice;
    char end = 0;

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    while (!end) {
        puts("=== Library Simulator ===");
        print_stock();
        printf("\n");
        puts("b: borrow a book");
        puts("r: return a book");
        puts("R: read a book");
        puts("q: quit");
        printf("> ");

        choice = getchar();
        while (getchar() != '\n') {}

        switch (choice) {
            case 'b':
                printf("Title length: ");

                scanf("%d", &size);
                getchar();

                if (size >= sizeof(title)) {
                    puts("The title is too long");
                } else {
                    printf("Title: ");
                    read_input(title, size-1);
                    borrow_book(title);
                }

                break;

            case 'r':
                printf("Title length: ");

                scanf("%d", &size);
                getchar();

                if (size >= sizeof(title)) {
                    puts("The title is too long");
                } else {
                    printf("Title: ");
                    read_input(title, size-1);
                    return_book(title);
                }

                break;

            case 'R':
                printf("Reading...");
                sleep(3);
                break;

            case 'q':
                end = 1;
                break;
            
            default:
                break;
        }
    }

    return EXIT_SUCCESS;
}
