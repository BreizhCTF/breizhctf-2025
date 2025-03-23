# Breizh Boot

Dans ce challenge, vous devez créer un disque virtuel qui contient une fitImage, une signature et une clé publique RSA 1024.
Le but est d'arriver à contourner le mécanisme de secure-boot mis en place, afin de lire le flag contenu dans un second disque de la machine virtuelle.

## Breizh-Boot #3

Le script suivant est executé par Barebox et permet de réaliser le secure-boot.

```sh
#!/bin/sh

# Define color escape codes
BLUE="\e[34m"
RED="\e[31m"
RESET="\e[0m"

# Define file paths
FITIMAGE="/mnt/virtioblk0/fitImage"
SIGNATURE="/mnt/virtioblk0/signature.bin"
PUBKEY="/mnt/virtioblk0/pubkey.breizhcertificate"

# Check each file individually
if [ ! -f "$FITIMAGE" ]; then
    echo -e "${RED}[BREIZH-BOOT] File not found: $FITIMAGE! Powering off...${RESET}"
    poweroff
fi

if [ ! -f "$SIGNATURE" ]; then
    echo -e "${RED}[BREIZH-BOOT] File not found: $SIGNATURE! Powering off...${RESET}"
    poweroff
fi

if [ ! -f "$PUBKEY" ]; then
    echo -e "${RED}[BREIZH-BOOT] File not found: $PUBKEY! Powering off...${RESET}"
    poweroff
fi

# Check using custom command if the fitImage is signed
breizhsecboot /mnt/virtioblk0/fitImage /mnt/virtioblk0/signature.bin /mnt/virtioblk0/pubkey.breizhcertificate
RES=$?
echo "Result is: $RES"
if [ $RES -ne 0 ]; then
    echo -e "${RED}Update script integrity check failed! Powering off...${RESET}"
    poweroff
fi

echo "Wp! Now we boot :)"
bootm /mnt/virtioblk0/fitImage

```

La commande `breizhsecboot` a été développée, et voici son code source :

```c
// BreizhCTF 2025 / BreizhBoot 3 / Drahoxx

/* breizhsecboot.c - Secure Boot Verification */
#include <common.h>
#include <command.h>
#include <fs.h>
#include <malloc.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <crypto/sha.h>
#include <crypto/rsa.h>
#include <crypto/pbl-sha.h>

#define MAX_BUFF_SIZE 256
#define HEADER "BZH.CERT\0"

// Hardcoded SHA256 of public key (equivalent to fuse mecanism in iMX6)
static uint8_t FUSE_0[SHA256_DIGEST_SIZE] = {
    0xc2, 0x26, 0x8f, 0x1f, 0xfb, 0x1c, 0x0c, 0x17, 
    0x2c, 0xf7, 0x7a, 0xfc, 0x9d, 0xaf, 0xb9, 0xff, 
    0xa7, 0x0f, 0x34, 0x5a, 0xaf, 0xde, 0x2d, 0x7a, 
    0x45, 0x26, 0x1d, 0xab, 0xb4, 0x0a, 0xdf, 0xc3
};
static uint8_t FUSE_1[SHA256_DIGEST_SIZE] = {
    0x13, 0x84, 0xd0, 0xe3, 0xb3, 0x1e, 0x3c, 0xcc, 
    0x9b, 0x08, 0x8d, 0xd4, 0x2c, 0xa2, 0xe0, 0xf8, 
    0x91, 0x91, 0x7f, 0x51, 0xe0, 0x8d, 0x6e, 0xee, 
    0x23, 0xef, 0xbc, 0x90, 0xe0, 0xbb, 0x8e, 0xb5
};
static uint8_t FUSE_2[SHA256_DIGEST_SIZE] = {
    0xdf, 0x98, 0x46, 0x61, 0x6c, 0x05, 0x83, 0x29, 
    0x49, 0xe4, 0x24, 0x7e, 0x03, 0xf5, 0x55, 0xe7, 
    0xcd, 0x7f, 0xeb, 0x45, 0xb3, 0xfa, 0xfb, 0x09, 
    0xe5, 0xf3, 0xce, 0x8f, 0xab, 0x83, 0xc5, 0x83
};

/**
 * parse_pubkey() - Parse an RSA public key from a binary file.
 * @file_path: Path to the binary file containing the RSA public key.
 * @p_rsa_key: Pointer to the RSA public key structure to be filled.
 *
 * Reads the public key components (modulus, exponent, n0inv, rr) from 
 * the file and stores them in dynamically allocated memory. Also verifies 
 * the presence of a valid header and key identifier.
 *
 * Returns 0 on success or -1 on error.
 */

static int parse_pubkey(const char *file_path, struct rsa_public_key *p_rsa_key) {
    char buff[MAX_BUFF_SIZE] = {0};
    int fd = open(file_path, O_RDONLY);
    int i;
    uint32_t len_key_id;
    uint64_t rsa_pub_exponent;
    uint32_t rsa_n0inv;
    uint32_t *rsa_rr;
    uint32_t *rsa_pub_modulus;
    
    printf("[VERBOSE] &parse_pubkey=%p\n", &parse_pubkey);


    rsa_rr = (uint32_t *)malloc(32 * sizeof(uint32_t));
    rsa_pub_modulus = (uint32_t *)malloc(32 * sizeof(uint32_t));

     if (fd < 0) {
        perror("Failed to open file");
        return -1;
    }

    // Magic bytes
    read(fd, buff, 8);
    if (strncmp(buff, HEADER, 8) != 0) {
        printf("Error: Wrong header.\n");
        close(fd);
        return -1;
    }

    // rsa_pub_exponent
    read(fd, &rsa_pub_exponent, 8);
    // rsa_n0inv
    read(fd, &rsa_n0inv, 4);
    // rsa_rr
    for(i = 0; i<32; i++ ){
        read(fd, &rsa_rr[i], 4);
    }
    // rsa_pub_modulus
    for(i = 0; i<32; i++ ){
        read(fd, &rsa_pub_modulus[i], 4);
    }

    // len_key_id
    read(fd, &len_key_id, 4);
    
    if (len_key_id < 1) {
        printf("Error: no key identifier or too short.\n");
        close(fd);
        return -1;
    }

    // key_id
    buff[read(fd, buff, len_key_id)] = '\0';
    close(fd);

    p_rsa_key->len = 32;                    /* Number of 32-bit words; 1024 bits / 32 = 32 words */
    p_rsa_key->modulus = rsa_pub_modulus;   /* RSA modulus */
    p_rsa_key->exponent = rsa_pub_exponent; /* RSA public exponent */
    p_rsa_key->n0inv = rsa_n0inv;
    p_rsa_key->rr = rsa_rr;

    printf("using key: %s\n",buff);

    return 0;  // Success
}

/**
 * read_file_to_buffer() - Read an entire file into a malloc'ed buffer.
 * @path: File path.
 * @buf:  Pointer to store the allocated buffer.
 * @size: Pointer to store the file size.
 *
 * Returns 0 on success or -1 on error.
 */
static int read_file_to_buffer(const char *path, uint8_t **buf, size_t *size)
{
    int fd;
    int ret;
    struct stat st;

    fd = open(path, O_RDONLY);
    if (fd < 0) {
        printf("Error: cannot open file: %s\n", path);
        return -1;
    }

    ret = fstat(fd, &st);
    if (ret < 0) {
        printf("Error: cannot stat file: %s\n", path);
        close(fd);
        return -1;
    }

    *size = st.st_size;
    *buf = malloc(*size);
    if (!*buf) {
        printf("Error: malloc failed for file: %s\n", path);
        close(fd);
        return -1;
    }

    ret = read(fd, *buf, *size);
    if (ret != *size) {
        printf("Error: read failed for file: %s\n", path);
        free(*buf);
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}

/**
 * verify_pubkey_hash() - check if pubkey's hash is hardcoded in hardware fuses (simulated)
 * @brief Check if the computed public key hash matches any stored fuses.
 *
 * @param computed_hash_pubkey Pointer to the computed hash.
 * @return int 1 if a match is found, 0 otherwise.
 */
static int verify_pubkey_hash(const uint8_t *computed_hash_pubkey) {
    if (memcmp(computed_hash_pubkey, FUSE_0, SHA256_DIGEST_SIZE) == 0) {
        return 1;
    }
    if (memcmp(computed_hash_pubkey, FUSE_1, SHA256_DIGEST_SIZE) == 0) {
        return 1;
    }
    if (memcmp(computed_hash_pubkey, FUSE_2, SHA256_DIGEST_SIZE) == 0) {
        return 1;
    }
    return 0;
}

/* Equivalent of main in barebox :) */
static int do_breizhsecboot(int argc, char *argv[])
{
    u8 *fitimage_buffer = NULL;
    u8 *signature_buffer = NULL;
    u8 *pubkey_buffer = NULL;
    size_t image_size, signature_size, pubkey_size;
    struct sha256_state sha_state = { 0 };
    struct digest d = { .ctx = &sha_state };
    uint8_t computed_hash_fitImage[SHA256_DIGEST_SIZE];
    uint8_t computed_hash_pubkey[SHA256_DIGEST_SIZE];
    struct rsa_public_key my_rsa_pub_key;
    int ret;

    /* Check argument count */
    if (argc < 4) {
        printf("Usage: breizhsecboot <fitImage_path> <signature_path> <cert_path>\n");
        return -1;
    }


    /* Read the FIT image into memory */
    if (read_file_to_buffer(argv[1], &fitimage_buffer, &image_size) < 0)
        return -1;

    /* Compute SHA‑256 digest of the FIT image */
    sha256_init(&d);
    sha256_update(&d, fitimage_buffer, image_size);
    sha256_final(&d, computed_hash_fitImage);
    

    /* Read the RSA signature into memory */
    if (read_file_to_buffer(argv[2], &signature_buffer, &signature_size) < 0) {
        free(fitimage_buffer);
        return -1;
    }

    /* Parse (pseudo)-certificate informations */
    if (parse_pubkey(argv[3], &my_rsa_pub_key) != 0) {
        return -1;
    }

    /* Read the public key file into memory */
    if (read_file_to_buffer(argv[3], &pubkey_buffer, &pubkey_size) < 0) {
        free(fitimage_buffer);
        free(pubkey_buffer);
        return -1;
    }

    /* Compute SHA‑256 digest of the public key file */
    sha256_init(&d);
    sha256_update(&d, pubkey_buffer, pubkey_size);
    sha256_final(&d, computed_hash_pubkey);

    /* Verify that the given key has been fused in the board to assure it's a legit key */
    if (verify_pubkey_hash(computed_hash_pubkey) == 0) {
        printf("Error: Public Key isn't fused.");
        free(fitimage_buffer);
        free(pubkey_buffer);
        free(signature_buffer);
        return -1;
    }

    /* Verify that the signature length matches the RSA key length.
     * For a 1024-bit key, expected length is 32 words * 4 bytes = 128 bytes.
     */
    if (signature_size != (my_rsa_pub_key.len * sizeof(uint32_t))) {
        printf("Error: invalid signature length. Expected %u bytes.\n",
               my_rsa_pub_key.len * (uint32_t)sizeof(uint32_t));
        free(fitimage_buffer);
        free(pubkey_buffer);
        free(signature_buffer);
        return -1;
    }

    /* Perform RSA signature verification.
     * rsa_verify() returns 0 on success.
     */
    ret = rsa_verify(&my_rsa_pub_key, signature_buffer, signature_size, computed_hash_fitImage, HASH_ALGO_SHA256);
    if (ret != 0) {
        printf("Secure boot error, signature unmatched.\n");
        free(fitimage_buffer);
        free(signature_buffer);
        return -1;
    }

    /* Clean up allocated memory */
    free(fitimage_buffer);
    free(signature_buffer);

    /* Signature verified successfully */
    return 0;
}

/* Register the breizhsecboot command with the Barebox command infrastructure */
BAREBOX_CMD_START(breizhsecboot)
    .cmd        = do_breizhsecboot,
    BAREBOX_CMD_DESC("breizhsecboot <fitImage_path> <signature_path> <cert_path>")
    BAREBOX_CMD_GROUP(CMD_GRP_MISC)
    BAREBOX_CMD_HELP("Verify FIT image using RSA secure boot")
BAREBOX_CMD_END
```

## Interractions (remote)
Vous pouvez utiliser le script `client.py` afin d'intéragir avec le challenge, ou bien directement via `nc`.

## Interractions (local)
Dans ce challenge, il peut être pratique de lancer le challenge directement, pour ce faire, la commande qemu suivante pourra vous être utile.

```bash
qemu-system-riscv64 -M virt -serial stdio -kernel files/barebox-dt-2nd.img -drive file=disk.img,format=raw,id=hd0 -device virtio-blk-device,drive=hd0 -drive file=fake-flag.img,format=raw,media=disk,id=hd1 -device virtio-blk-device,drive=hd1 -m 300M
```

Le challenge a été testé sur la version suivante de Qemu (repos apt ubuntu 24.04.1 LTS) :
```bash
$ qemu-system-riscv64 --version
QEMU emulator version 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.4)
Copyright (c) 2003-2023 Fabrice Bellard and the QEMU Project developers
```

## Commandes utiles
### Formatage du disque
Le disque à envoyer doit être formaté avec un filesystem FAT. Ce disque est monté sur le point de montage `/mnt/virtioblk0/` dans barebox.
```bash
dd if=/dev/zero of=disk.img bs=1M count=10
mkfs.vfat disk.img
mkdir -p mntpt
sudo mount -o loop disk.img mntpt/
```

### Génération de clé et certificats
La signature implémentée utilise RSA 1024, les commandes suivantes permettent de générer une clé privée via openssl, de signer une image et aussi de retranscrire la clé publique dans un format compris par `breizhsecboot`.
```bash
# Gen keys
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:1024
# Sign image
openssl dgst -sha256 -sign private.pem -out signature.bin fitImage
# Convert to BreizhCertificate
python3 convert-pem-to-breizhcertificate.py private.pem pubkey.breizhcertificate <String Key identifier>
```
Bon courage !