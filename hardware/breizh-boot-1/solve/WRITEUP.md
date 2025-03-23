# BreizhBoot #1

Le but est d'avoir une fitImage qui a un crc32 de 0x13371337.

## Solve

Si on veut "brute-force" le crc, cela trop trop long (~6h). Il y a donc une seconde méthode.

En effet, le crc32 est réversible.

Une recherche "DuckDuckGo" avec "brute force crc32" donne : https://www.nayuki.io/res/forcing-a-files-crc-to-any-value/forcecrc32.py

Cela permet de forcer le CRC d'un fichier sans brute-force (uniquement mathématiquement). Il suffit de modifier 4 bytes du fichier. Les derniers bytes de la fitImage sont tous nulles et ne servent pas. On peut donc les éditer pour faire matcher le crc32.

`python3 forcecrc32.py fitImage 8511173 13371337`

On peut checker le crc avec la commande Linux `crc32 fitImage`.

Ensuite on envoie l'image :
`python3 client.py fitImage breizh.ctf 1337`


## Admin test
L'image fitGood a le bon crc32.

**Flag :**
> BZHCTF{CRC_ain't_S3curity_JusT_Safety} 
