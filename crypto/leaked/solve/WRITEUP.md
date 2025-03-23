# Leaked

Le challenge consiste à retrouver la clé privée en analysant la consommation électrique lors du calcul de la clé publique.

Cette génération, basée sur la fonction `scalar_mult()` utilise l'algorithme Double and Add. Celui-ci effectue 1 opération (Double) si le bit est à 0, contre 2 opérations (Double and Add) si le bit est à 1.

On retrouver ce comportement dans la trace.

Il semble y avoir des blocks de :
- 3*100 points entre 1.5 et 2.5,
- 1*100 points < 0
- 2*100 points > 2.5

Le script python explique la méthode de parsing et de résolution.

```python
import numpy as np
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

file_path = "trace.txt"  # Replace with actual file path
with open(file_path, "r") as f:
    trace = np.array([float(line.strip()) for line in f])

"""
On regarde la moyenne par block de 100 pour voir le comportement

for i in range(0,4000,100):
    print(np.mean(trace[i:i+100]))

...
1.73166096
2.12781593
2.13129011
-0.5090924200000001
3.02671877
3.25115076
-0.41134534
2.1160464300000004
2.2725360000000006
2.0651315500000003
-0.63154942
...

Il semble y avoir des blocks de :
- 3*100 points entre 1.5 et 2.5,
- 1*100 points < 0
- 2*100 points > 2.5

L'algorithme "double and add" effectue 2 opérations lorsque le bit est à 1.
Un 1 est donc représenté dans la trace par un bloc moyen et un bloc haut.
"""

key = ""

i = 0
while i < len(trace):
    m = np.mean(trace[i:i+100])

    if m > 2.5:
        key += "1"
        i += 200
    elif m > 1.5:
        key += "0"
        i += 300
    else:
        i += 100

key = key.replace("01", "1")

private_key = int(key[::-1], 2)
print(private_key)

def decrypt_message(encrypted_message, private_key):
    key = hashlib.sha256(str(private_key).encode()).digest()
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

enc = bytes.fromhex("85df4965181aeec6cacf3c023d5be68f29854924f4aa39bf9731ecf33872d32cfaf4c4af7daee0e31ea5faa47c8848f91a8707bb7f0db4ed118d98f07a0434344d435edd1000fc901848147d5cc9106b")

print(decrypt_message(enc,private_key))
```