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