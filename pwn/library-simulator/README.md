# pwn - Library Simulator

```sh
./gen_files.sh
docker build -t library_simulator -f src/Dockerfile src
docker run --rm -it -p 1337:1337 library_simulator
[...]
docker rmi library_simulator
```
