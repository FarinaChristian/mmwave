import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import mmwave as mm
import mmwave.dsp as dsp
from mmwave.dataloader import DCA1000
from mmwave.tracking import EKF
import cv2
import os

# Radar specific parameters
NUM_RX = 4
VIRT_ANT = 8

# Data specific parameters
NUM_CHIRPS = 128
NUM_ADC_SAMPLES = 128
RANGE_RESOLUTION = .0488
DOPPLER_RESOLUTION = 0.0806
NUM_FRAMES = 250

# DSP processing parameters
SKIP_SIZE = 4
ANGLE_RES = 1
ANGLE_RANGE = 90
ANGLE_BINS = (ANGLE_RANGE * 2) // ANGLE_RES + 1
BINS_PROCESSED = 112

# Funzione per progettare un filtro passa banda
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Funzione per applicare il filtro
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

adc_data = np.fromfile('destra_sinistra.bin', dtype=np.uint16)    
adc_data = adc_data.reshape(NUM_FRAMES, -1)
#divido i segnali arrivati, all_data è un array di array tridimensionali
all_data = np.apply_along_axis(DCA1000.organize, 1, adc_data, num_chirps=NUM_CHIRPS*2, num_rx=NUM_RX, num_samples=NUM_ADC_SAMPLES)

fs = 10000.0  # Frequenza di campionamento della scheda 
filtrati=[]   #contiene i segnali filtrati, è un array di array
magazzino=[]  #conterrè le trasformate dei singoli segnali filtrati, è un array di array
# Specifiche del filtro passa banda, sono i valori per i battiti
lowcut = 0.8 #Hz
highcut = 4 #Hz

'''STRUTTURA DI UN FRAME:
       Sono 250 frame, un frame è un array tridimensionale e contiene 256 matrici (penso sia perchè 128*2=256).
       Ogni matrice contiene 4 array di lunghezza 128, questi array dovrebbero essere i segnali da analizzare.
       [ [ [2,5,....,70]  [ [2,5,....,70]  [ [2,5,....,70]      [ [2,5,....,70]      
           [2,5,....,70]    [2,5,....,70]    [2,5,....,70] .....  [2,5,....,70]
           [2,5,....,70]    [2,5,....,70]    [2,5,....,70]        [2,5,....,70]
           [2,5,....,70] ]  [2,5,....,70] ]  [2,5,....,70] ]      [2,5,....,70] ] ]'''

for frame in all_data: 
    for matrice in frame:
        for segnale in matrice:       
            # Applicare il filtro ai segnali interessati contenuti nei frame 
            filtered_sig = bandpass_filter(segnale, lowcut, highcut, fs)#è monodimensionale
            filtrati.append(filtered_sig)
            #eseguo la trasformata del segnale nel frame
            fft_signal=radar_cube = mm.dsp.range_processing(filtered_sig)#è monodimensionale
            magazzino.append(fft_signal)

'''for frame in all_data:
    # Variabili temporanee per ciascun frame
    segnali_filtrati_frame = []
    segnali_trasformati_frame = []

    # Ciclo per ogni matrice nel frame (senza scendere a livello di segnale individuale)
    for matrice in frame:
        # Applica il filtro e la trasformata a tutti i segnali della matrice
        segnali_filtrati_matrice = [bandpass_filter(segnale, lowcut, highcut, fs) for segnale in matrice]
        segnali_trasformati_matrice = [mm.dsp.range_processing(sig) for sig in segnali_filtrati_matrice]

        # Aggiunge i risultati della matrice al frame
        segnali_filtrati_frame.extend(segnali_filtrati_matrice)
        segnali_trasformati_frame.extend(segnali_trasformati_matrice)

    # Aggiunge i risultati del frame completo alle liste finali
    filtrati.extend(segnali_filtrati_frame)
    magazzino.extend(segnali_trasformati_frame)'''

# Visualizzare il segnale originale e quello filtrato
plt.figure(figsize=(10, 8)) 
plt.subplot(3, 1, 1)  
plt.plot(all_data[0][0, 0, :], color='orange')
plt.title('Segnale originale')
plt.xlabel('Tempo')
plt.ylabel('Ampiezza')
plt.grid()
plt.legend()

# Terzo grafico: FFT del segnale originale o filtrato
plt.subplot(3, 1, 2) 
plt.plot(filtrati[0])
plt.title('Segnale filtrato con filtro passa banda')
plt.xlabel('Tempo')
plt.ylabel('Ampiezza')
plt.grid()
plt.legend()

# Secondo grafico: Segnale originale
plt.subplot(3, 1, 3)  # 3 righe, 1 colonna, secondo grafico
plt.plot(np.abs(magazzino[0]),color='green')
plt.title('Ftt del segnale filtrato')
plt.xlabel('Campioni')
plt.ylabel('Ampiezza')
plt.grid()
plt.legend()

# Mostrare tutti i grafici
plt.tight_layout()  # Ottimizza il layout per evitare sovrapposizioni
plt.show()

