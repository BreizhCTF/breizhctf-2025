from PIL import Image

def transformation_du_cliche_photomaton(image_source):
    x_prime, y_prime = (0, 0)

    width, height = image_source.size
    image_output = Image.new("RGBA", (width, height))

    pixel_source = image_source.load()
    pixel_output = image_output.load()

    for y in range(0, height, 2):
        x_prime = 0
        for x in range(0, width, 2):
            UL = pixel_source[x, y]
            UR = pixel_source[x+1, y]
            DL = pixel_source[x, y+1]
            DR = pixel_source[x+1, y+1]

            pixel_output[x_prime, y_prime] = UL
            pixel_output[x_prime + (width//2), y_prime] = UR
            pixel_output[x_prime, y_prime + (height//2)] = DL
            pixel_output[x_prime + (width//2), y_prime + (height//2)] = DR

            x_prime += 1

        y_prime += 1

    return image_output

