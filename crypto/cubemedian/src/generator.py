import qrcode
import numpy as np
from PIL import Image
import random
from secret import flag


def next_seed(seed):
    return int(str(seed**3).zfill(8)[2:10])


def generate_qr(data):
    qr = qrcode.make(data)
    return np.array(qr)


def save_qr_image(qr_array, filename):
    img = Image.fromarray(qr_array)
    img = img.convert("L")
    img.save(filename)


def encrypt_qr(qr_array, seed):
    size = qr_array.shape[0]

    assert size == 410

    seq = []
    for _ in range(size):
        seed = next_seed(seed)
        seq.append(seed)

    encrypted = qr_array.copy()
    
    for i, rand in enumerate(seq):
        swap_idx = rand % size
        encrypted[[i, swap_idx]] = encrypted[[swap_idx, i]]
    
    return encrypted


seed = 6202711

for _ in range(random.randint(2**12, 2**13)):
    seed = next_seed(seed)

qr = generate_qr(flag)

encrypted_qr = encrypt_qr(qr, seed)
save_qr_image(encrypted_qr, "encrypted_flag.png")