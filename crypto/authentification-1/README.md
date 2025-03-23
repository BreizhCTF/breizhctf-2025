Ciphertext forgery avec un AES-GCM mal implémenté (nonce reused + pas de verif d'auth).
Niveau Facile

```
docker build . --tag auth
docker run -p 80:80 -it auth
```

