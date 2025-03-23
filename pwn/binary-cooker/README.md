# Binary Cooker
Niveau très difficile.

```
./gen_files.sh
docker build -t binary_cooker .
docker run --rm -it -p 1337:1337 --name binary_cooker binary_cooker
[...]
docker kill binary_cooker
docker rmi binary_cooker
```
