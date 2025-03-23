# Breizh Boot

Bienvenue dans cette suite de challenge nommée **Breizh-Boot**. Le but de ces challenges est simple : contourner le secure-boot mis en place.

## Breizh-Boot #1
Le premier challenge vise à contourner le secure-boot suivant :

```sh
#!/bin/sh

# barebox/defaultenv/defaultenv-2-base/init/_secure_boot.sh

# Define color escape codes
BLUE="\e[34m"
RED="\e[31m"
RESET="\e[0m"

echo -e "${BLUE}[BREIZH-BOOT]${RESET} Starting boot in secure-mode!"

# Mount partition
mkdir -p /boot
mount /dev/virtioblk0 /boot

# Run CRC32 (from barebox) with verification
crc32 -f /boot/fitImage -v 0x13371337
sh
# Check if CRC32 command failed
if [ $? -ne 0 ]; then
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} CRC verification ${RED}failed${RESET}! Powering off..."
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} CRC must match ${RED}0x13371337${RESET}"
    poweroff
fi

# CRC check passed, proceed with boot
echo -e "${BLUE}[BREIZH-BOOT]${RESET} CRC verification passed! Booting..."
bootm /boot/fitImage
```

L'instruction `bootm` permet de lancer linux et donc obtenir le flag (si l'image n'est pas corrompue...) !

## Infra
Ce challenge met en place divers mécanismes afin de démarrer une image Linux via un secure-boot personnalisé.

--------    -----------    -----------      ---------    ----------------
| QEMU | -> | OpenSBI | -> | Barebox |  ->  | Linux | -> | cat flag.txt |
--------    -----------    -----------  /\  ---------    ----------------
                     ---------------------------------------
                      Script de vérification du secure-boot
                      (vérifie si la fitImage est conforme)
                             -----------------------

1. qemu-system-riscv64
Qemu est le logiciel qui permet de virtualiser un processeur, des périphériques, etc. Ici, une puce risc-v avec 2 disques est simulé. Le premier disque contient le flag dans un système de fichier EXT-4. Le deuxième disque contient une **fitImage** dans un système de fichier FAT.

Une **fitImage** contient :
- Kernel Linux (compressé)
- InitRD créé avec busybox (compressé)
- Device Tree Blob (virt qemu)

Qemu va donc simuler le matériel, mais aussi démarrer un pré-bootloader (OpenSBI) qui va lancer barebox.

2. Barebox
Barebox est un bootloader, c'est la première pièce logicielle qu'on contrôle. Le bootloader va faire les étapes suivantes :
    1. Vérification de l'intégrité de la fitImage (secure-boot personnalisé) ;
    2. Extraction des différents éléments de la fitImage, puis les charger en RAM ;
    3. Sauter sur le kernel afin de démarrer le système d'exploitation.

3. Linux
Le linux intégré dans la fitImage fournie va ouvrir le second disque automatiquement et afficher le flag.

Le script d'initialisation pour Linux (/init) est le suivant :
```sh
#!/bin/sh
echo "#### WELCOME IN BREIZH-Linux ###"

echo " ______                 _         _           _        _                "      
echo "(____  \               (_)       | |         | |      (_)                     "
echo " ____)  )  ____   ____  _  _____ | | _   ___ | |       _  ____   _   _  _   _ "
echo "|  __  (  / ___) / _  )| |(___  )| || \ (___)| |      | ||  _ \ | | | |( \ / )"
echo "| |__)  )| |    ( (/ / | | / __/ | | | |     | |_____ | || | | || |_| | ) X ( "
echo "|______/ |_|     \____)|_|(_____)|_| |_|     |_______)|_||_| |_| \____|(_/ \_)"

# Populate rootfs
mkdir /proc /sys /tmp
mount -t proc none /proc
mount -t sysfs none /sys
mount -t tmpfs none /tmp

# Populate /dev
mdev -s

# Mount flag drive
mkdir /mnt
mount /dev/vdb /mnt

echo -e "\nFlag is: \n"
cat /mnt/flag.txt

/bin/sh
poweroff
```

4. Client.py
Le fichier `client.py` permet d'intéragir plus facilement avec le serveur afin d'envoyer votre fitImage et démarrer la puce.

```
eg. python3 client.py fitImage bzh.ctf 1337

usage: client.py [-h] file_path ip port

Client for flashing and booting a RISC-V chip.

positional arguments:
  file_path   Path to fitImage file
  ip          Server IP
  port        Server port

options:
  -h, --help  show this help message and exit
```

Vous pouvez aussi utiliser un netcat (`nc`) afin d'intéragir directement avec le serveur.

```
Menu:
1. Flash chip memory
2. Boot chip
3. Kill all QEMU processes running
4. Exit
```

## Test en local
1. Extraire les fichiers du challenge
`tar xvzf breizh_boot_1.tar.gz`
2. Modifier le fichier `fitImage`
3. Lancer le setup du challenge via `docker compose up --build`
4. Tester votre solution : `python3 client.py fitImage localhost 1337`

Si vous avez résolu le challenge, vous devriez voir le flag s'afficher.
```
Flag is:

BZHCTF{Fake_Flag_For_Testing}
```

Vous pouvez ensuite utiliser `client.py` sur l'instance du BreizhCTF, pour récupérer le vrai flag sur le serveur.

## Tips & Tricks
- N'essayez pas de recréer votre propre fitImage, la compilation de Linux & de busybox est très longue. Essayez de modifier l'image fournie.
- Pensez à la planète, éteignez le docker, et le qemu dès que vous arrêtez de l'utiliser (option 3 du serveur afin de kill les qemu qui tournent).
- Testez en local avant de tester en remote, ces challenges prennent beaucoup de ressources.

