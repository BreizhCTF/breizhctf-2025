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
