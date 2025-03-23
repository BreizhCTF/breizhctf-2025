#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <signal.h>

#define die(msg) do { \
        dprintf(STDERR_FILENO, "%s\n", msg); \
        exit(EXIT_FAILURE); \
    } while (0)


#define LISTEN_PORT 1337
#define DELIM ","
#define STACK_SIZE 16


void sigint_handler(int x) {
    exit(EXIT_SUCCESS);
}


typedef struct session_s {
    char *alloc_buf;
    char *buf;
    char *stack[STACK_SIZE];
    ssize_t stack_idx;
} session_t;



session_t *new_session() {
    session_t *s = malloc(sizeof(*s));
    if (!s) die("new_session: allocation failed");
    memset(s, 0, sizeof(*s));

    s->stack_idx = -1;
    return s;
}

void del_session(session_t *s) {
    if (!s) return;
    free(s->alloc_buf);

    for (int i = 0; i < STACK_SIZE; i++) {
        if (s->stack[i] != s->alloc_buf) {
            free(s->stack[i]);
        }
    }

    free(s);
}

void push(session_t *s) {
    if (s->stack_idx == (STACK_SIZE - 1)) {
        puts("push: the stack is full");
        return;
    }

    if (!s->buf) {
        s->stack[++s->stack_idx] = NULL;
    } else {
        s->stack[++s->stack_idx] = strdup(s->buf);
    }
}

void pop(session_t *s) {
    if (s->stack_idx == -1) {
        puts("pop: the stack is empty");
    } else {
        s->buf = s->stack[s->stack_idx--];
    }
}

void split(session_t *s, char *delim) {
    char *ret = strtok(s->buf, delim);
    if (ret != NULL) {
        s->buf = ret;
    }
}

void next_token(session_t *s, char *delim) {
    char *ret = strtok(NULL, delim);

    if (ret == NULL) {
        puts("next_token: no more tokens");
    } else {
        s->buf = ret;
    }
}

void new_input(session_t *s) {
    char buf[256] = {0};
    size_t n = 0;

    printf("buffer: ");
    fflush(stdout);

    fgets(buf, sizeof(buf), stdin);

    if (!s->buf || strlen(s->buf) < strlen(buf)) {
        s->alloc_buf = strdup(buf);
        s->buf = s->alloc_buf;
    } else {
        strcpy(s->buf, buf);
    }
}


void help() {
    puts("help:");
    puts("    i: new input");
    puts("    h: hex encode");
    puts("    H: hex decode");
    puts("    s: split");
    puts("    n: next token");
    puts("    u: url encode");
    puts("    U: url decode");
    puts("    p: push");
    puts("    P: pop");
    puts("    r: reset session");
    puts("    ?: show help");
    puts("    q: quit");
}


int handle_client() {
    char end = 0;
    char choice;
    session_t *s = new_session();

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    printf("initial ");
    new_input(s);

    help();

    while (!end) {
        printf("buf: %s\n> ", s->buf);
        fflush(stdout);

        choice = getchar();
        if (choice != 0xa) {
            getchar(); // skip the new line
        }

        switch (choice) {
            case 0xa:
                break;
            case 'q':
                end = 1;
                break;
            case 'i':
                new_input(s);
                break;
            case 'h':
            case 'H':
                puts("not implemented");
                break;
            case 's':
                split(s, DELIM);
                break;
            case 'n':
                next_token(s, DELIM);
                break;
            case 'u':
            case 'U':
                puts("not implemented");
                break;
            case 'p':
                push(s);
                break;
            case 'P':
                pop(s);
                break;
            case 'r':
                del_session(s);
                s = new_session();
                break;
            case '?':
            default:
                help();
                break;
        }
    }

    puts("bye!");
    return EXIT_SUCCESS;
}

int main() {
    signal(SIGINT, sigint_handler);

    // socket
    int sfd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sfd == -1) {
        perror("socket");
        die("");
    }

    // setsockopt to prevent "Address already in use"
    int enabled = 1;
    if (0 != setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &enabled, sizeof(int))) {
        perror("setsockopt");
        close(sfd);
        die("");
    }

    // bind
    struct sockaddr_in saddr = {0};
    saddr.sin_family = AF_INET;
    if (NULL != getenv("CHALL_IS_IN_CONTAINER")) {
        // needed to be able to reach the challenge from outside of the container
        saddr.sin_addr.s_addr = htonl(INADDR_ANY);
    } else {
        saddr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    }
    saddr.sin_port = htons(LISTEN_PORT);
    if (0 != bind(sfd, (struct sockaddr *)&saddr, sizeof(saddr))) {
        perror("bind");
        close(sfd);
        die("");
    }

    // listen
    if (0 != listen(sfd, 8)) {
        perror("listen");
        close(sfd);
        die("");
    }

    printf("listening on port %d\n", LISTEN_PORT);

    // accept
    struct sockaddr_in caddr;
    socklen_t caddr_len = sizeof(caddr);
    while (1) {
        int cfd = accept(sfd, (struct sockaddr *)&caddr, &caddr_len);
        int child_pid = 0;

        printf(".");
        fflush(stdout);

        child_pid = fork();

        if (child_pid == 0) {
            // child process
            dup2(cfd, STDIN_FILENO);
            dup2(cfd, STDOUT_FILENO);
            dup2(cfd, STDERR_FILENO);

            handle_client();

            shutdown(cfd, SHUT_WR);
            close(cfd);
            exit(EXIT_SUCCESS);
        } else {
            // parent process
            waitpid(child_pid, NULL, 0);
        }
    }
}
