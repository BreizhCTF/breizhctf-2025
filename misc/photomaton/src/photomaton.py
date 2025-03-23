# Implémente le procédé : https://fr.wikipedia.org/wiki/Transformation_du_clich%C3%A9_Photomaton
from do_it_yourself import transformation_du_cliche_photomaton as tdcp
from PIL import Image

flag = Image.open("flag.png")
for _ in range(13):
    flag = tdcp(flag)

flag.save("goodluck.png")

