from do_it_yourself import transformation_du_cliche_photomaton as tdcp
from math import lcm, log2
from sys import argv
from PIL import Image

if len(argv) != 2:
    print("usage : python solve.py <path_output_img>")
    exit(1)

out_img = Image.open(argv[1])

w, h = out_img.size
periode = lcm(int(log2(w)), int(log2(h)))

for _ in range(periode - 13):
    out_img = tdcp(out_img)

out_img.show()

