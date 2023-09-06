import cv2
import os
import time
import glob
import numpy as np

# Imposta la directory corrente
current_directory = os.getcwd()

# Definisci il pattern da cercare
pattern = "frame_*.png"

# Rimuovi tutti i file che corrispondono al pattern
for file in os.scandir(current_directory):
    if file.name.startswith("frame_") and file.name.endswith(".png"):
        os.remove(file.path)

# Rimuovi tutti i file che corrispondono al pattern
for file in os.scandir(current_directory):
    if file.name.startswith("diff_") and file.name.endswith(".png"):
        os.remove(file.path)

time.sleep(1)

# Attendi che la directory sia completamente svuotata
while any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
    pass
while any(fname.startswith("diff_") for fname in os.listdir(current_directory)):
    pass

# Attendi che la directory sia completamente svuotata
while True:
    # Controlla se ci sono file che corrispondono al pattern
    if any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
        print("La directory non è vuota.")
        # Attendi un secondo e verifica nuovamente
        time.sleep(1)
    else:
        print("La directory è vuota.")
        # Nessun altro file corrisponde al pattern, esci dal ciclo
        break

# Il resto del tuo codice va qui

# Apre il video
videoFile = 'C:\\Users\\mdegi\\OneDrive\\Desktop\\Work\\FMD\\video\\Braq10_05sec.mp4'
cap = cv2.VideoCapture(videoFile)

# Legge il primo frame
ret, frame = cap.read()
# Mostra il primo frame
cv2.imshow('Seleziona ROI', frame)
# Seleziona la ROI con il mouse
x, y, w, h = cv2.selectROI('Seleziona ROI', frame, False)
# Salva le coordinate della prima ROI come riferimento
ref_x, ref_y, ref_w, ref_h = x, y, w, h

# Chiude la finestra per la selezione della ROI
cv2.destroyAllWindows()

counter = 0
while True:
    # Legge un frame video
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

# Calcola le differenze tra le immagini adiacenti
diff_images = []
valid_diff_images = []
for i in range(len(images) - 1):

    # Calcola la differenza tra le immagini
    diff = cv2.absdiff(images[i], images[i+1])
    diff_images.append(diff)

    _, bin_diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    # Controlla se l'immagine binarizzata contiene informazioni valide
    if np.any(bin_diff):
        valid_diff_images.append(diff)
        diff_images.append(diff)  # Aggiungi tutte le immagini di differenza alla lista

# Visualizza le immagini di differenza valide come un video continuo
frame_rate = 50
for diff in valid_diff_images:
    cv2.imshow("Difference Image", diff)
    if cv2.waitKey(int(1000 / frame_rate)) == ord('q'):
        break

# Accumulazione dei frame validi in un'immagine accumulativa
if valid_diff_images:
    accumulated_image = valid_diff_images[0].copy()
    for i in range(1, len(valid_diff_images)):
        accumulated_image += valid_diff_images[i]

    # Visualizza l'immagine accumulativa
    cv2.imshow("Accumulated Image", accumulated_image)
    # Salva l'immagine accumulativa come file, se necessario
    cv2.imwrite("accumulated_image.png", accumulated_image)

# Svuota la directory dei file che iniziano con "frame"
for file in os.scandir(current_directory):
    if file.name.startswith("frame_") and file.name.endswith(".png"):
        os.remove(file.path)

# Attendi l'input dell'utente per chiudere l'immagine
cv2.waitKey(0)
cv2.destroyAllWindows()

# Chiusura del video e del programma
cap.release()


