import numpy as np
import matplotlib.pyplot as plt
import mmwave as mm
from mmwave.dataloader import DCA1000
from matplotlib.widgets import Button, TextBox

# Inizializzazione del DCA1000
dca = DCA1000()

# Funzione per aggiornare i limiti dell'asse x
def update_xlim(val):
    try:
        new_xlim = int(text_box.text)  # Ottiene il valore dalla casella di testo
        new_xlim2 = int(text_box2.text)  
        new_xlim3 = int(text_box3.text)  
        new_ylim = int(text_boxy.text)  
        new_ylim2 = int(text_box2y.text)  
        new_ylim3 = int(text_box3y.text)  
        ax.set_xlim(0, new_xlim)  # Imposta il nuovo limite dell'asse x
        ax2.set_xlim(0, new_xlim2)  
        ax3.set_xlim(0, new_xlim3)  
        ax.set_ylim(0, new_ylim)  # Imposta il nuovo limite dell'asse y
        ax2.set_ylim(0, new_ylim2)  
        ax3.set_ylim(0, new_ylim3)  
        fig.canvas.draw()  # Aggiorna il grafico
    except ValueError:
        print("Inserisci un numero valido")

# Configura il grafico
plt.ion()  # Abilita la modalità interattiva
fig, (ax, ax2,ax3) = plt.subplots(3, 1, figsize=(10, 10))
line, = ax.plot([], [])
line2, = ax2.plot([], [],color='green')
line3, = ax3.plot([], [],color='orange')

ax.set_xlim(0, 100)  # Imposta i limiti dell'asse x
ax.set_ylim(0, 700)  # Imposta i limiti dell'asse y
ax.set_xlabel('Tempo')
ax.set_ylabel('Ampiezza')
ax.set_title('Dominio del tempo')

ax2.set_xlim(0, 1000)  # Imposta i limiti dell'asse x
ax2.set_ylim(0, 40000)  # Imposta i limiti dell'asse y
ax2.set_xlabel('Distanza')
ax2.set_ylabel('Potenza')
ax2.set_title('FTT')

ax3.set_xlim(0, 1000)  # Imposta i limiti dell'asse x
ax3.set_ylim(0, 30000000)  # Imposta i limiti dell'asse y
ax3.set_xlabel('Velocità')
ax3.set_ylabel('Distanza')
ax3.set_title('FTT2')

plt.subplots_adjust(hspace=0.4)

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
axbox = plt.axes([0.1, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box = TextBox(axbox, 'X: ', initial="100")
text_box.label.set_color("blue")

axboxy = plt.axes([0.15, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_boxy = TextBox(axboxy, 'Y: ', initial="700")
text_boxy.label.set_color("blue")

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
ax2box = plt.axes([0.3, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box2 = TextBox(ax2box, 'X: ', initial="1000")
text_box2.label.set_color("green")

ax2boxy = plt.axes([0.35, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box2y = TextBox(ax2boxy, 'Y: ', initial="40000")
text_box2y.label.set_color("green")

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
ax3box = plt.axes([0.5, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box3 = TextBox(ax3box, 'X: ', initial="1000")
text_box3.label.set_color("orange")

ax3boxy = plt.axes([0.55, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box3y = TextBox(ax3boxy, 'Y: ', initial="30000000")
text_box3y.label.set_color("orange")

# Creazione del pulsante
ax_button = plt.axes([0.7, 0.02, 0.08, 0.035])  # Posizione e dimensione del pulsante
button = Button(ax_button, 'Aggiorna')

# Collega la funzione di aggiornamento al clic del pulsante
button.on_clicked(update_xlim)

# Inizializzazione dei dati
x_data = np.arange(3000)  # 100 punti dati
y_data = np.zeros(3000)   # Inizializza i dati a zero

# Inizializzazione dei dati
x_data2 = np.arange(3000)  # 100 punti dati
y_data2 = np.zeros(3000)   # Inizializza i dati a zero

# Inizializzazione dei dati
x_data3 = np.arange(3000)  # 100 punti dati
y_data3 = np.zeros(3000)   # Inizializza i dati a zero

while True:
    # Leggi i dati dal DCA1000
    adc_data = dca.read()

    # Applica la FFT utilizzando range_processing
    radar_cube = mm.dsp.range_processing(adc_data)
    # Applica la FFT2 utilizzando range_processing
    radar_cube2 = mm.dsp.range_processing(radar_cube)
    
    if adc_data is not None:
        # Aggiorna i dati
        y_data = adc_data[:3000]/100  # Supponiamo che adc_data sia un array di almeno 100 elementi
        y_data2 = np.abs(radar_cube[:3000]/1000)
        y_data3 = np.abs(radar_cube2[:3000]/1000)

        # Aggiorna il grafico
        line.set_ydata(y_data)
        line.set_xdata(x_data)

        # Aggiorna il grafico della ftt
        line2.set_ydata(y_data2)
        line2.set_xdata(x_data2)

        # Aggiorna il grafico della velocità
        line3.set_ydata(y_data3)
        line3.set_xdata(x_data3)

        fig.canvas.draw()
        fig.canvas.flush_events()
    else:
        print("Nessun dato ricevuto.")

    
    # Ora puoi applicare un'altra FFT sull'output di 'range_processing', ad esempio su un'altra dimensione
    # Se volessi fare una FFT su un'altra dimensione, per esempio sugli assi dei chirp o delle antenne:
    #fft_on_radar_cube = np.fft.fft(radar_cube, axis=0)  # FFT lungo l'asse dei chirp
    # Oppure, se vuoi applicarla lungo l'asse delle antenne
    #fft_on_radar_cube_antennas = np.fft.fft(radar_cube, axis=1)  # FFT lungo l'asse delle antenne

    #adc_data = adc_data.reshape(300, -1)
    #frame = dca.organize(adc_data, 128, 4, 500) #num_chirps=NUM_CHIRPS*2 num_rx=NUM_RX num_samples=NUM_ADC_SAMPLES