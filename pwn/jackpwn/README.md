# Jackpwn

```sh
./gen_files.sh
docker build -t jackpwn -f src/Dockerfile .
docker run --rm -it -p 1337:1337 jackpwn
[...]
docker rmi jackpwn
```
