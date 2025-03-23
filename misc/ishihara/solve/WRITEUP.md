BreizhCTF 2025 - Ishihara
==========================

### Challenge details

| Event                    | Challenge  | Category       | Points | Solves      |
|--------------------------|------------|----------------|--------|-------------|
| BreizhCTF 2025           | Ishihara   | Stéganographie | ???    | ???         |

![colorblind](https://media1.tenor.com/m/tV1izjyb0zoAAAAC/donkey-shrek.gif)

Ce serait tellement plus facile si je n'étais pas daltonien !

Auteur : [Zeecka](https://x.com/zeecka_)

- Fichier: [Ishihara.zip](../dist/Ishihara.zip)
- md5sum: a78fd4433b9fa59abaa971b78f5171ff

### TL;DR

Le challenge est un [Test d'Ishihara](https://fr.wikipedia.org/wiki/Test_d%27Ishihara) inversé.
L'ajout de filtres de simulation de daltonisme, ou le remapping des couleurs laisse apparaitre les lettres composant le flag.

### Méthodologie

Le contenu de l'archive présente un ensemble d'images semblables aux tests de daltonismes (en particulier les [tests chromatiques d'Ishihara](https://fr.wikipedia.org/wiki/Test_d%27Ishihara)).

![archive_content](./img/archive_content.png)

Il est cepend très difficile d'identifier un quelconque chiffre parmis les différentes planches.

L'application d'[un filtre de simulation de daltonisme](https://www.color-blindness.com/coblis-color-blindness-simulator/) de type Protanopie et Deuteranopie permet de mettre en évidence la présence de formes distinctes semblables à des lettres.

*Note : Les personnes daltoniennes sont légèrement avantagées dans la découverte de ces formes.*

![3B](./img/3B.png)

> Exemple du filtre lettre "B" (première lettre du format de flag).

### Méthode 0 - Super Héro

Cette méthode consiste à trouver un volontaire dans son équipe, de péférence daltonien, pour identifier les lettres de chaque images sans aucune transformation 🤡. Cette personne devra alors passer sa nuit à torturer ses yeux pour la gloire de son équipe.

![superman](https://media1.tenor.com/m/rnEtl9S1Yz4AAAAC/superman-and-lois-superman.gif)

### Méthode 1 - Random colors remapping

L'utilisation du célèbre logiciel [StegSolve](http://www.caesum.com/handbook/Stegsolve.jar) permet de remapper les couleurs d'une image de manière aléatoire à l'aide de sa vue "Random colour map".

![random_color_map](./img/random_color_map.png)

![random_color_map2](./img/random_color_map2.png)

> Exemple du filtre lettre "B" (première lettre du format de flag).

Compte tenu du caractère aléatoire du remapping, la répétition des tentatives de mapping permet d'aboutir a des lettres facilement perceptibles.

Une fois l'ensemble des lettres décodées, on récupère le flag : `BZHCTF{1shih4rA_?never_he4rd_ab0ut!}`

### Méthode 2 - Custom colors remapping

La méthode la plus adaptée pour résoudre le challenge consiste à identifier les couleurs composant les lettres, et celles composant le fond de planche.

Pour cela, deux solutions. La première repose sur l'utilisation de l'outil pipette (disponible sur paint, navigateur, ...) pour récupérer les différents code couleurs.

La deuxième solution consiste à parser les images pixel par pixel, et ajouter chaque nouvelle couleur à une liste. Les couleurs découvertes en premiers correspondent à celles utilisées pour le fond de plance, tandisque les dernières correspondent aux lettres.

On utilisera pour cela le langage python et sa bibliothèque [Pillow](https://pypi.org/project/pillow/).

```python
#!/usr/bin/env python3

from PIL import Image
import zipfile

def main():
    archive = zipfile.ZipFile('../dist/Ishihara.zip', 'r')
    flag_size = len(archive.namelist())  # Nombre de lettres

    new_colors = []
    zip_img = archive.open(f"0.png")  # On récupère la première image
    img = Image.open(zip_img)
    img_data = img.getdata()  # On lit ses pixels
    for color in img_data:
        if color not in new_colors:
            new_colors.append(color)
            print(color)  # On affiche les couleurs dans l'ordre de découverte

if __name__ == "__main__":
    main()
```

```text
(255, 255, 255)
(190, 185, 103)
(232, 14, 38)
(216, 159, 104)
(77, 188, 119)
(252, 138, 39)
(159, 169, 44)
(29, 163, 48)
(167, 127, 65)
(219, 113, 29)
(154, 50, 15)
(228, 177, 150)
(233, 127, 103)
(104, 188, 64)
(118, 98, 87)
(159, 170, 154)
(149, 195, 131)
```

On identifie ainsi les 11 premières couleurs comme étant les couleurs de fond, et les 6 dernières celles composant les lettres.

On procède ensuite au remapping des couleurs, toujours à l'aide d'un script python et de la bibliothèque Pillow:

```python
#!/usr/bin/env python3

from PIL import Image
import zipfile

# On identifie toutes les couleurs qui sont "autour" des lettres.
BAD_COLORS = [
    (255, 255, 255),
    (190, 185, 103),
    (232, 14, 38),
    (216, 159, 104),
    (77, 188, 119),
    (252, 138, 39),
    (159, 169, 44),
    (29, 163, 48),
    (167, 127, 65),
    (219, 113, 29),
    (154, 50, 15)
]

def main():
    archive = zipfile.ZipFile('../dist/Ishihara.zip', 'r')
    flag_size = len(archive.namelist())  # Nombre de lettres
    flag_image = Image.new('1', (800 * flag_size, 800))  # Image vierge de la taile du flag

    for i in range(flag_size):  # Pour chaque image de l'archive
        zip_img = archive.open(f"{i}.png")
        img = Image.open(zip_img)
        img_data = img.getdata()  # On lit ses pixels
        filtered_image = Image.new('1', img.size)
        filtered_data = []  # On créer son équivalent "filtré"
        for color in img_data:  # On parcour chaque pixels et on ajoute un pixel
            if color not in BAD_COLORS: # noir ou blanc en fonction des couleurs
                filtered_data.append(0)
            else:
                filtered_data.append(1)
        filtered_image.putdata(filtered_data)
        flag_image.paste(filtered_image, (800*i, 0))  # On ajoute la lettre au flag

    flag_image.save("flag.png")
    flag_image.show()

if __name__ == "__main__":
    main()
```

Le résultat est le suivant : 

![flag.png](./img/flag.png)


#### Flag

`BZHCTF{1shih4rA_?never_he4rd_ab0ut!}`

### Notes de l'auteur

La création du challenges est basée sur les références suivantes:

- Article : https://isohedral.ca/dichromatic-steganography/
- Papier : https://archive.bridgesmathart.org/2023/bridges2023-173.html
- Hidden Plates: https://www.color-blind-test.com/color-blind-tests/ishihara-test/hidden-plates.html
- LSM Space viewer : https://daltonlens.org/understanding-cvd-simulation/
- Tests : https://daltonlens.org/colorblindness-simulator
- Outil : https://github.com/nikooo777/ColorBlind/
- Exemple twitter : https://x.com/IsaacKing314/status/1795495558225739905
- Article lié au tweet : https://mymodernmet.com/reverse-ishihara-vision-test/