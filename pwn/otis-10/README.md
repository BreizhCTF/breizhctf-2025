# Otis 10

```sh
./gen_files.sh
docker build -t otis_10 -f src/Dockerfile .
docker run --rm -it -p 1337:1337 otis_10
[...]
docker rmi otis_10
```
