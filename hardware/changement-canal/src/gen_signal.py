import numpy as np
from scipy.io.wavfile import write

message = "_LES_CANAUX_CTCSS_NE_SONT_PAS_CONFIDENTIELS_DU_TOUT____________________________________________________________"

ctcss_frequencies = [67.0, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rate = 44100
letter_duration = 3

def generer_signal(frequence, duree, taux_echantillonnage, amplitude):
    t = np.linspace(0, duree, int(taux_echantillonnage * duree), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequence * t)
    return signal

signal = np.zeros(0)


for letter in message:
    if letter == "_":
        signal = np.concatenate((signal, np.zeros(letter_duration * rate)))
    else:
        frequency = ctcss_frequencies[alphabet.index(letter)]
        signal = np.concatenate((signal, generer_signal(frequency, letter_duration, rate, 1)))

# Normalisation pour sauvegarde dans un fichier WAV (amplitude entre -32767 et 32767)
signal_normalise = np.int16(signal * 32767)

# Sauvegarde dans un fichier WAV
nom_fichier = "ctcss.wav"
write(nom_fichier, rate, signal_normalise)


