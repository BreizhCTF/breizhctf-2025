import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

def charger_wav(fichier_wav):
    taux_echantillonnage, signal = wav.read(fichier_wav)
    return taux_echantillonnage, signal

def decouper_tranches(signal, taux_echantillonnage, duree_tranche):
    taille_tranche = int(taux_echantillonnage * duree_tranche)
    return [signal[i:i + taille_tranche] for i in range(0, len(signal), taille_tranche)]

def analyser_fft(signal, taux_echantillonnage, plage_frequences=(67, 163)):
    # Calcul de la FFT
    taille_signal = len(signal)
    freqs = np.fft.rfftfreq(taille_signal, d=1/taux_echantillonnage)
    fft_vals = np.abs(np.fft.rfft(signal))
    
    # Filtrer pour garder seulement les fréquences dans la plage désirée
    masque = (freqs >= plage_frequences[0]) & (freqs <= plage_frequences[1])
    freqs_filtrees = freqs[masque]
    fft_vals_filtrees = fft_vals[masque]
    
    # Trouver la fréquence avec la plus grande amplitude
    freq_max = freqs_filtrees[np.argmax(fft_vals_filtrees)]
    amplitude_max = np.max(fft_vals_filtrees)
    return freq_max, amplitude_max

def afficher_resultats(resultats):
    ctcss_frequencies = [67.0, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i, (freq, amplitude) in enumerate(resultats):
        letter = "_"
        for i in range(26):
            if abs(freq - ctcss_frequencies[i]) < 0.2:
                letter = alphabet[i]
                break
        print(letter, end="")
    print()

def analyser_fichier_wav(fichier_wav, duree_tranche=5):
    taux_echantillonnage, signal = charger_wav(fichier_wav)
    
    tranches = decouper_tranches(signal, taux_echantillonnage, duree_tranche)
    
    resultats = []
    for tranche in tranches:
        freq_max, amplitude_max = analyser_fft(tranche, taux_echantillonnage)
        resultats.append((freq_max, amplitude_max))
    
    afficher_resultats(resultats)

fichier_wav = "record.wav"
analyser_fichier_wav(fichier_wav, duree_tranche=3)
