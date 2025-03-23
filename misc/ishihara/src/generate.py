#!/usr/bin/env python3

import os
import math
import random
import sys
import argparse
import logging
import numpy as np
import tqdm
from PIL import Image, ImageFont, ImageDraw
from colorlog import ColoredFormatter
from scipy.spatial import cKDTree as KDTree

DEFAULT_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                  "abcdefghijklmnopqrstuvwxyz" \
                  "0123456789_-+}{!?"
FONT_FAMILY = "KaushanScript-Regular.otf"
WIDTH, HEIGHT = 800, 800
FONT_SIZE = 550
BACKGROUND = (255, 255, 255)
TOTAL_CIRCLES = 1200

color = lambda c: ((c >> 16) & 255, (c >> 8) & 255, c & 255)
COLORS_ON_1 = [
    color(0x9faa9a), color(0xe4b196), color(0x95c383)
]
COLORS_OFF_1 = [
    color(0xd89f68), color(0xbeb967), color(0x4dbc77),
    color(0x4dbc77), color(0xa77f41)
]
COLORS_ON_2 = [
    color(0x766257), color(0x68bc40), color(0xe97f67)
]
COLORS_OFF_2 = [
    color(0x9a320f), color(0xfc8a27), color(0x1da330),
    color(0xdb711d), color(0xe80e26), color(0x9fa92c)
]


def get_parser():
    """ Return argument parser for the generate script. """
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Generate reversed Ishiara plates',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    parser_a = subparsers.add_parser('letters', help='Generate letters images',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_a.add_argument('-c', '--chars', help="Charset to generate", default=DEFAULT_CHARSET)

    parser_b = subparsers.add_parser('plates', help='Generate plates images',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_b.add_argument('-n', type=int, help='Number of generated plates per letters', default=4)
    parser_b.add_argument('-c', '--chars', help="Charset to generate", default=DEFAULT_CHARSET)

    parser_c = subparsers.add_parser('flag', help='Generate plates with a given flag',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_c.add_argument('-f', '--flag', help="Flag to generate", required=True)

    parser.add_argument('-v', '--verbose', help="Be verbose",
        action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO
    )

    return parser

def format_logger(log_level):
    """ Format script logger. """
    global log
    LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)
    log = logging.getLogger('generate')
    log.setLevel(log_level)
    log.addHandler(stream)

# LETTERS

def generate_letters(charset):
    """ Saves images of each letters for a given charset. """
    log.info(f"Generating {len(charset)} PNG letters.")
    for l in tqdm.tqdm(charset):
        log.debug(f"Generating letters: {l}")
        img = create_letter(l)
        img.save("./letters/"+l+'.png')

def create_letter(letter):
    """ Create a PIL Image containing a given letter """
    font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
    image = Image.new('1', (WIDTH,HEIGHT), 1)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), letter, font=font)
    draw.text(((WIDTH-w)/2, (HEIGHT-h)/2-80), letter, font=font)
    return image

# PLATES

def generate_plates(charset, count):
    """ Generate n ishihara plates for a given charset. """
    log.info(f"Generating {len(charset)*count} Ishihara plates.")
    for l in tqdm.tqdm(charset, desc="Letter : ", position=0):
        for i in range(count):
            img = generate_letter_plate(l)
            img.save(f"./ishihara/{l}_plate{i+1}.png")

def generate_circle(image_width, image_height, min_diameter, max_diameter):
    """ Generate circle for ishihara. """
    radius = random.triangular(min_diameter, max_diameter,
                               max_diameter * 0.8 + min_diameter * 0.2) / 2

    angle = random.uniform(0, math.pi * 2)
    distance_from_center = random.uniform(0, image_width * 0.48 - radius)
    x = image_width  * 0.5 + math.cos(angle) * distance_from_center
    y = image_height * 0.5 + math.sin(angle) * distance_from_center

    return x, y, radius


def overlaps_motive(image, circle):
    """ Verify if circle will overlaps with the letter. """
    x, y, r = circle
    points_x = [x, x, x, x-r, x+r, x-r*0.93, x-r*0.93, x+r*0.93, x+r*0.93]
    points_y = [y, y-r, y+r, y, y, y+r*0.93, y-r*0.93, y+r*0.93, y-r*0.93]

    for xy in zip(points_x, points_y):
        if image.getpixel(xy)[:3] != BACKGROUND:
            return True

    return False


def circle_intersection(circle1, circle2):
    """ Verify if circle with overlap with an other """
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    return (x2 - x1)**2 + (y2 - y1)**2 < (r2 + r1)**2


def circle_draw(draw_image, image, circle):
    """ Draw the circle on the image with random colors. """
    COLORS_ON = COLORS_ON_1
    COLORS_OFF = COLORS_OFF_1
    if random.randint(0,1):
        COLORS_ON = COLORS_ON_2
        COLORS_OFF = COLORS_OFF_2

    fill_colors = COLORS_ON if overlaps_motive(image, circle) else COLORS_OFF
    fill_color = random.choice(fill_colors)

    x, y, r = circle
    draw_image.ellipse((x - r, y - r, x + r, y + r),
                       fill=fill_color,
                       outline=fill_color)

def generate_letter_plate(l):
    """ Generate ishihara image plate for a given letter. """
    log.debug(f"Generating plate {l}.")
    try:
        image = Image.open("./letters/"+l+".png").convert('RGB')
    except:
        log.error(f"Letter {l} doesn't exist. Creating the letter...")
        generate_letters(l)

    image = Image.open("./letters/"+l+".png").convert('RGB')
    image2 = Image.new('RGB', image.size, BACKGROUND)
    draw_image = ImageDraw.Draw(image2)
    width, height = image.size
    min_diameter = (width + height) / 220
    max_diameter = (width + height) / 60
    circle = generate_circle(width, height, min_diameter, max_diameter)
    circles = [circle]
    circle_draw(draw_image, image, circle)
    for _ in range(TOTAL_CIRCLES):
        tries = 0
        kdtree = KDTree([(x, y) for (x, y, _) in circles])
        while True:
            circle = generate_circle(width, height, min_diameter, max_diameter)
            elements, indexes = kdtree.query([(circle[0], circle[1])], k=12)
            for element, index in zip(elements[0], indexes[0]):
                if not np.isinf(element) and circle_intersection(circle, circles[index]):
                    break
            else:
                break
            tries += 1

        circles.append(circle)
        circle_draw(draw_image, image, circle)
    return image2

# FLAG

def generate_flag(flag):
    """ Generate ishihara plates in the right order for a given flag. """
    log.info(f"Generating challenge for flag: {flag}")
    log.debug(f"Remove previous png in challenge directory")
    os.system("rm -f ./challenge/*.png")
    for n, l in enumerate(tqdm.tqdm(flag)):
        img = generate_letter_plate(l)
        img.save(f"./challenge/{n}.png")


def main():
    """ Main function, route argument parser. """
    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    format_logger(args.loglevel)

    if args.command == "letters":
        generate_letters(args.chars)
    elif args.command == "plates":
        generate_plates(args.chars, args.n)
    elif args.command == "flag":
        generate_flag(args.flag)

if __name__ == "__main__":
    main()
