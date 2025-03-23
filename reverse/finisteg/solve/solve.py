import argparse
import base64
from PIL import Image

def binary_to_string(binary_text):
    chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_text = []
    channels = [0, 1, 2]  # R, G, B channels

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            channel = channels[len(binary_text) % 3]
            value = pixel[channel] & 1  # Extract LSB
            binary_text.append(str(value))

            if len(binary_text) % 8 == 0 and ''.join(binary_text[-8:]) == "00000000":
                return binary_to_string(''.join(binary_text[:-8]))

    return "Aucun texte trouvé"

def main():
    parser = argparse.ArgumentParser(description="Extract hidden text from an image using LSB steganography.")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()

    extracted_text = extract_text_from_image(args.image_path)
    print("Extracted text:", extracted_text)

    try:
        flag = base64.b64decode(extracted_text).decode('utf-8')
        print("Flag:", flag)
    except Exception as e:
        print("Error decoding base64:", e)

if __name__ == "__main__":
    main()

