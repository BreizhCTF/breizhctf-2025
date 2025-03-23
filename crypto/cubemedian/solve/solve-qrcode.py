import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
from tqdm import tqdm

def next_seed(seed):
    return int(str(seed**3).zfill(8)[2:10])


def unscramble_qr(scrambled_array, seed):
    size = scrambled_array.shape[0]
    seq = []
    for _ in range(size):
        seed = next_seed(seed)
        seq.append(seed)
    
    unscrambled = scrambled_array.copy()
    
    for i in reversed(range(len(seq))):
        swap_idx = seq[i] % size
        unscrambled[[i, swap_idx]] = unscrambled[[swap_idx, i]]

    return unscrambled


def qr_image_to_array(image_path):
    img = Image.open(image_path).convert("L") 
    img = img.resize((410, img.height), Image.NEAREST)

    qr_array = np.array(img)
    return qr_array

def extract_qr_data(img):
    decoded_objects = decode(img)

    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    return None


for i in tqdm(range(2**12, 2**13)):
    seed = 6202711

    for _ in range(i):
        seed = next_seed(seed)

    qr = qr_image_to_array("../files/encrypted_flag.png")
    flag = unscramble_qr(qr, seed)
    img = Image.fromarray(flag)
    img = img.convert("L")
    qr_data = extract_qr_data(img)
    if not (qr_data is None) and ("BZHCTF" in qr_data): 
        print("Extracted Data:", qr_data)
        print(i)
        break
