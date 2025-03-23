Chiffrement : Time Locked Encryption
https://people.csail.mit.edu/rivest/pubs/RSW96.pdf

Vulnérabilité : attaque sur PRNG : https://eprint.iacr.org/2021/1204.pdf

``` 
sudo docker build . -t locked
sudo docker run --rm --name locked -p 1337:1337 locked
``` 
