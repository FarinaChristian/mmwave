import numpy as np
import matplotlib.pyplot as plt
import mmwave as mm
from mmwave.dataloader import DCA1000
from matplotlib.widgets import Button, TextBox, CheckButtons

# Funzione per aggiornare i limiti dell'asse x e y
def update_xlim(val):
    try:
        ax.set_xlim(int(text_box.text.split(",")[0].strip()),int(text_box.text.split(",")[1].strip()))
        ax.set_ylim(int(text_boxy.text.split(",")[0].strip()),int(text_boxy.text.split(",")[1].strip()))
        ax2.set_xlim(int(text_box2.text.split(",")[0].strip()),int(text_box2.text.split(",")[1].strip()))
        ax2.set_ylim(int(text_box2y.text.split(",")[0].strip()),int(text_box2y.text.split(",")[1].strip()))
        ax3.set_xlim(int(text_box3.text.split(",")[0].strip()),int(text_box3.text.split(",")[1].strip()))
        ax3.set_ylim(int(text_box3y.text.split(",")[0].strip()),int(text_box3y.text.split(",")[1].strip()))
      
        fig.canvas.draw()  # Aggiorna il grafico
    except ValueError:
        print("Inserisci un numero valido")

def avviaCattura(val):
    guardia=False
    dca=None
    adc_data=None
    try:
        # Inizializzazione del DCA1000
        dca = DCA1000()
        guardia=True
        plt.ion()  # Abilita la modalità interattiva
    except:
        print("Nessuna scheda collegata")

    while guardia:
        try:
            # Leggi i dati dal DCA1000
            adc_data = dca.read()
        except TimeoutError:
            print("LETTURA TERMINATA")
            plt.ioff()#disabilito la modalità interattiva
            break

        # Applica la FFT utilizzando range_processing
        radar_cube = mm.dsp.range_processing(adc_data)
        
        # Applica la FFT2 utilizzando range_processing
        radar_cube2 = mm.dsp.range_processing(np.abs(radar_cube))#gli passo il grafico delle ampiezze, se gli passassi tutta la trasformata ottengo la sinusoide iniziale specchiata
        
        if adc_data is not None:
            # Aggiorna i dati
            y_data = adc_data / 100  # Divido gli elementi dentro l'array per scalarli

            #decido se rappresentare la fase o l'ampiezza, falso-->ampiezza vero--->fase
            if(check.get_status()[0]==False):
                y_data2 = np.abs(radar_cube / 10000)
                ax2.set_title('FTT Ampiezza')
            else:
                y_data2 = np.angle(radar_cube / 10000)
                ax2.set_title('FTT2 Fase')

            if(check.get_status()[1]==False):
                y_data3 = np.abs(radar_cube2 / 10000000)
                ax3.set_title('FTT2 Ampiezza')
            else:
                y_data3 = np.angle(radar_cube2 / 10000000)
                ax3.set_title('FTT2 Fase')

             # Aggiorna il grafico
            line.set_ydata(y_data)
            line.set_xdata(x_data)

            # Aggiorna il grafico della ftt
            line2.set_ydata(y_data2)
            line2.set_xdata(x_data2)

            # Aggiorna il grafico della ftt2
            line3.set_ydata(y_data3)
            line3.set_xdata(x_data3)

            fig.canvas.draw()
            fig.canvas.flush_events()
        else:
            print("Nessun dato ricevuto.")

# Configura i grafici
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
ax2.set_ylim(0, 4000)  # Imposta i limiti dell'asse y
ax2.set_xlabel('Distanza')
ax2.set_ylabel('Potenza')
ax2.set_title('FTT Ampiezza')

ax3.set_xlim(0, 500)  # Imposta i limiti dell'asse x
ax3.set_ylim(0, 10000)  # Imposta i limiti dell'asse y
ax3.set_xlabel('Velocità')
ax3.set_ylabel('Distanza')
ax3.set_title('FTT2 Ampiezza')

plt.subplots_adjust(hspace=0.4)

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
axbox = plt.axes([0.1, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box = TextBox(axbox, 'X: ', initial="0,100")
text_box.label.set_color("blue")

# Creazione della casella di testo per inserire il nuovo limite dell'asse y
axboxy = plt.axes([0.15, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_boxy = TextBox(axboxy, 'Y: ', initial="0,700")
text_boxy.label.set_color("blue")

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
ax2box = plt.axes([0.3, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box2 = TextBox(ax2box, 'X: ', initial="0,1000")
text_box2.label.set_color("green")

# Creazione della casella di testo per inserire il nuovo limite dell'asse y
ax2boxy = plt.axes([0.35, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo [left,bottom,width,height]
text_box2y = TextBox(ax2boxy, 'Y: ', initial="0,4000")
text_box2y.label.set_color("green")

# Creazione della casella di testo per inserire il nuovo limite dell'asse x
ax3box = plt.axes([0.5, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box3 = TextBox(ax3box, 'X: ', initial="0,500")
text_box3.label.set_color("orange")

# Creazione della casella di testo per inserire il nuovo limite dell'asse y
ax3boxy = plt.axes([0.55, 0.02, 0.04, 0.035])  # Posizione e dimensione della casella di testo
text_box3y = TextBox(ax3boxy, 'Y: ', initial="0,10000")
text_box3y.label.set_color("orange")

# Creazione del pulsante per cambiare le dimensioni
ax_button = plt.axes([0.7, 0.02, 0.08, 0.035])  # Posizione e dimensione del pulsante
button = Button(ax_button, 'Aggiorna')

# Creazione del pulsante per avviare la cattura
cat = plt.axes([0.8, 0.02, 0.08, 0.035])  # Posizione e dimensione del pulsante
cattura = Button(cat, 'Avvia')

# Creazione delle checkbox per decidere di rappresentare la fase o l'ampiezza
checkbox_ax = plt.axes([0.01, 0.3, 0.06, 0.3])  # Posizione e dimensione delle checkbox
check = CheckButtons(checkbox_ax, ['Fase FTT', 'Fase FTT2'], [False, False])

# Collega la funzione di aggiornamento e di cattura al clic dei pulsanti
button.on_clicked(update_xlim)
cattura.on_clicked(avviaCattura)

# Inizializzazione dei dati
x_data = np.arange(393216)  # 393216 è la dimension edell'array che mi arriva
y_data = np.zeros(393216)   # Inizializza i dati a zero

# Inizializzazione dei dati
x_data2 = np.arange(393216)  
y_data2 = np.zeros(393216)   

# Inizializzazione dei dati
x_data3 = np.arange(393216)  
y_data3 = np.zeros(393216)  

fig.canvas.draw()
plt.show()



