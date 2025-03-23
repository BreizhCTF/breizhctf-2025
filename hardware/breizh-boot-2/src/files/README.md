# Breizh Boot

Attention, ce challenge est différent du premier, cette fois-ci, vous devrez importer le disque entier et non pas uniquement la fitImage.


## Breizh-Boot #2

Le script suivant est executé par Barebox et permet de réaliser le secure-boot. À vous de le bypass ;)

```sh
#!/bin/sh

# Define color escape codes
BLUE="\e[34m"
RED="\e[31m"
RESET="\e[0m"

# Expected hashes
HASH_1="67392e3abf0588b4546a0b3a2b9773874fc0a2f8"
HASH_2="540756da504ceb6763c8f2821c51cd2147cedd6e"
HASH_3="b731ef942d879aeb2220bbde7ffe0d14e4fedfe1"
HASH_4="3670cae458b1cb2c6e2b0089bb9de6c2c693dbbd"
HASH_UPDATE="597d8205a49ec2129f8517761ac3619cbd7d906a"

# Mount disk
mount /dev/virtioblk0 /mnt/virtioblk0

# Menu
echo -e "${BLUE}[BREIZH-BOOT]${RESET} Select boot image:"
echo "1) fitImage-1"
echo "2) fitImage-2"
echo "3) fitImage-3"
echo "4) fitImage-4"
echo "Enter choice: "
readline ">> " choice

if [ "$choice" = "1" ]; then
    IMAGE="fitImage-1"; HASH="$HASH_1"
elif [ "$choice" = "2" ]; then
    IMAGE="fitImage-2"; HASH="$HASH_2"
elif [ "$choice" = "3" ]; then
    IMAGE="fitImage-3"; HASH="$HASH_3"
elif [ "$choice" = "4" ]; then
    IMAGE="fitImage-4"; HASH="$HASH_4"
elif [ "$choice" = "5" ]; then
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} Enter password: "
    readline ">> " password
    if [ "$password" != "root" ]; then
        echo -e "${RED}Incorrect password!${RESET}"
        poweroff
    fi
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} Running update script..."
    if [ ! -f "/mnt/virtioblk0/update.sh" ]; then
        echo -e "${RED}[BREIZH-BOOT] Update script not found! Powering off...${RESET}"
        poweroff
    fi
    digest -a sha1 -s "$HASH_UPDATE" "/mnt/virtioblk0/update.sh"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Update script integrity check failed! Powering off...${RESET}"
        poweroff
    fi
    sh /mnt/virtioblk0/update.sh
    exit 0
else
    echo -e "${RED}Invalid choice! Enter 1, 2, 3, 4.${RESET}"
    poweroff
fi

if [ ! -f "/mnt/virtioblk0/$IMAGE" ]; then
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} Selected image not found! Running default..."
    if [ ! -f "/mnt/virtioblk0/update.sh" ]; then
        echo -e "${RED}[BREIZH-BOOT] File script not found! Powering off...${RESET}"
        poweroff
    fi
    sh /mnt/virtioblk0/update.sh
    exit 0
fi

echo -e "${BLUE}[BREIZH-BOOT]${RESET} Verifying integrity of $IMAGE..."
digest -a sha1 -s "$HASH" "/mnt/virtioblk0/$IMAGE"

if [ $? -ne 0 ]; then
    echo -e "${BLUE}[BREIZH-BOOT]${RESET} Integrity check ${RED}failed${RESET}! Powering off..."
    poweroff
fi

# Yey, we boot
echo -e "${BLUE}[BREIZH-BOOT]${RESET} Integrity check passed! Booting $IMAGE..."
bootm "/mnt/virtioblk0/$IMAGE"
```

Vous pouvez utiliser le script `client.py` afin d'intéragir avec le challenge, ou bien directement via `nc`.


Le disque à envoyer doit être formaté avec un filesystem FAT. Ce disque est monté sur le point de montage `/mnt/virtioblk0/` dans barebox.
```sh
dd if=/dev/zero of=disk.img bs=1K count=50
mkfs.vfat disk.img
...
python3 client.py disk.img <host> <port>
```

Bon courage !
