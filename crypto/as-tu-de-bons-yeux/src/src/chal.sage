load("sanitize.sage")
load("utils.sage")

from os import getenv
FLAG = getenv("FLAG", "BZHCTF{censuré}")

print("Bienvenue, j'espère que tu as de bons yeux !")

count = 0
seuil = 128
for i in range(130):
    if count >= seuil:
        print(f"Bien joué, voici ton flag : {FLAG}")
        exit()

    (A, t), is_mlwe = get_instance()

    print(f"{sanitize_mat(A) = }")
    print(f"{sanitize_vec(t) = }")

    ans = int(input("MLWE (1) ou pas (0) ?\n> "))

    if ans == is_mlwe:
        count += 1
        print(f"wp, {count}/{seuil}")
    else:
        print(f"oups, {count}/{seuil}")

