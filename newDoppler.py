import cv2
import os
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
import shutil

# Imposta la directory corrente
current_directory = os.getcwd()

# Definisci il pattern da cercare
pattern = "frame_*.png"

# Rimuovi tutti i file che corrispondono al pattern
for file in os.scandir(current_directory):
    if file.name.startswith("frame_") and file.name.endswith(".png"):
        os.remove(file.path)


for file in os.scandir(current_directory):
    if file.name.startswith("plotDiff_"):
        os.remove(file.path)

for file in os.scandir(current_directory):
    if file.name.startswith("column_"):
        os.remove(file.path)

# Rimuovi la cartella "Difference images and Plot" e tutto il suo contenuto se esiste
output_directory = 'Difference images and Plot'
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)

time.sleep(1)

# Attendi che la directory sia completamente svuotata
while any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
    pass

# Apre il video
videoFile = 'C:\\Users\\mdegi\\OneDrive\\Desktop\\Work\\FMD\\video\\Braq10_10 sec.mp4'
cap = cv2.VideoCapture(videoFile)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Impossibile aprire il video.")
else:
    # Ottieni il numero totale di frame nel video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Ottieni il numero di frame al secondo (FPS) del video
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calcola la durata in secondi
    duration_seconds = total_frames / fps
    print(f"Durata del video: {duration_seconds} secondi")

# Leggi il primo frame
ret, frame_iniziale = cap.read()
# Mostra il primo frame
cv2.imshow('Seleziona ROI', frame_iniziale)
# Seleziona la ROI con il mouse
x, y, w, h = cv2.selectROI('Seleziona ROI', frame_iniziale, False)
# Salva le coordinate della prima ROI come riferimento
ref_x, ref_y, ref_w, ref_h = x, y, w, h

# Chiude la finestra per la selezione della ROI
cv2.destroyAllWindows()

counter = 0
while True:
    # Leggi un frame video
    ret, frame = cap.read()
    # Verifica se il frame è stato letto correttamente
    if not ret:
        break

    # Utilizza la ROI iniziale per tutti i frame
    roi = frame[ref_y:ref_y + ref_h, ref_x:ref_x + ref_w]

    # Salva la ROI come immagine
    filename = f'frame_{counter:04d}.png'
    if roi is not None and roi.size > 0:
        cv2.imwrite(filename, roi)
    else:
        print("Impossibile salvare l'immagine. ROI vuota o non valida.")

    counter += 1

    # Disegna la ROI sul frame corrente
    cv2.rectangle(frame, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (0, 255, 0), 2)

    # Mostra il frame
    cv2.imshow('Video con ROI', frame)

    # Esci dall'input se si preme 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Recupera i nomi dei file delle immagini che iniziano con "frame_" e terminano con ".png"
image_files = sorted(glob.glob("frame_*.png"))

# Carica le immagini dalla lista dei nomi dei file
images = []
previous_img = None  # Immagine precedente
for filename in image_files:
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    if previous_img is None or not np.array_equal(img, previous_img):
        images.append(img)
        previous_img = img

column_index = 0  # Inizializza l'indice della colonna
last_column_index = 0  # Inizializza l'indice dell'ultima colonna
stop_requested = False  # Variabile per controllare se è stata richiesta l'interruzione

# Lista per memorizzare i frame corrispondenti all'ultima colonna
last_column_frames = []

while column_index < ref_w:
    # Verifica se è stata richiesta l'interruzione
    if cv2.waitKey(1) == ord('q'):
        stop_requested = True
        break

    # Estrai la colonna corrente dalla ROI
    column = roi[:, column_index]

    # Salva la colonna come immagine
    filename = f'column_{column_index:04d}.png'
    cv2.imwrite(filename, column)

    # Aggiorna l'indice dell'ultima colonna
    last_column_index = column_index

    # Passa alla colonna successiva
    column_index += 1

    # Ritardo tra le iterazioni (regola la velocità)
    cv2.waitKey(25)  # Aggiungi un ritardo tra le colonne (25 millisecondi, ad esempio)

# Se è stata richiesta l'interruzione, salva il frame corrente
if stop_requested:
    last_column_frames.append(images[last_column_index][:, :last_column_index])

# Salva l'ultimo frame anche se non è stata richiesta l'interruzione
last_column_frames.append(images[-1][:, :last_column_index])

# Ora puoi utilizzare last_column_frames per avere il frame corrispondente all'ultima colonna
# indipendentemente da dove il ciclo sia stato interrotto
for i in range(len(images)):
    if i <= last_column_index:
        last_column_frames.append(images[i])
# Dopo aver raccolto tutte le immagini in last_column_frames
# Assicurati che tutte le immagini abbiano le stesse dimensioni
height, width = last_column_frames[0].shape[:2]
for i in range(len(last_column_frames)):
    last_column_frames[i] = cv2.resize(last_column_frames[i], (width, height))

# Unisci tutte le immagini in orizzontale
final_image = np.hstack(last_column_frames)

# Mostra l'immagine finale in una finestra
cv2.imshow('Immagine Finale', final_image)

# Crea una finestra per la visualizzazione del video
cv2.namedWindow('Video di Output', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video di Output', ref_w, ref_h)

# Itera attraverso le immagini e mostra il video con la ROI
for img in images:
    # Copia il frame corrente in una variabile separata
    frame_with_roi = img.copy()

    # Disegna la ROI sul frame corrente
    cv2.rectangle(frame_with_roi, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (0, 255, 0), 2)

    # Mostra il frame con la ROI
    cv2.imshow('Video di Output', frame_with_roi)

    # Esci dall'input se si preme 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Calcola le differenze tra le immagini adiacenti
diff_images = []
valid_diff_images = []
for i in range(len(images) - 1):

    # Calcola la differenza tra le immagini
    diff = cv2.absdiff(images[i], images[i+1])


    _, bin_diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    # Controlla se l'immagine binarizzata contiene informazioni valide
    if np.any(bin_diff):
        valid_diff_images.append(diff)
        diff_images.append(diff)  # Aggiungi tutte le immagini di differenza alla lista

# Creazione della directory per i file di output
output_directory = 'Difference images and Plot'
os.makedirs(output_directory, exist_ok=True)

# Salva solo le immagini di differenza valide nella directory "output"
for i, diff in enumerate(valid_diff_images):
    diff_filename = os.path.join(output_directory, f'diff_{i:04d}.png')
    cv2.imwrite(diff_filename, diff)

# Visualizza le immagini di differenza valide come un video continuo
frame_rate = 50
for diff in valid_diff_images:
    cv2.imshow("Difference Image", diff)
    if cv2.waitKey(int(1000 / frame_rate)) == ord('q'):
        break

# Rilascia la finestra solo dopo aver visualizzato tutte le immagini
cv2.destroyAllWindows()

# Calcolo delle somme delle colonne per le immagini di differenza
sums = []
for i, diff in enumerate(valid_diff_images):
    col_sum = np.sum(diff, axis=0)
    sums.append(col_sum)

    # Plotta l'andamento delle somme delle colonne
    plt.figure(figsize=(8, 6))
    plt.plot(col_sum, label=f'Immagine {i + 1}')
    plt.title(f'Andamento Somma Colonne - Immagine {i + 1}')
    plt.xlabel('Colonne')
    plt.ylabel('Somma')
    plt.legend()

    # Salva il plot in una directory specifica
    plot_filename = os.path.join(output_directory, f'plotDiff_{i:04d}.png')
    plt.savefig(plot_filename)
    plt.close()

# Chiusura del video e del programma
cap.release()

