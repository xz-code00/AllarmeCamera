import cv2
import face_recognition
import winsound

# Carica le immagini dei volti da riconoscere
immagine1 = face_recognition.load_image_file("saramin.jpeg")
immagine2 = face_recognition.load_image_file("luca.jpeg")

# Ottieni le codifiche dei volti da riconoscere
codifica1 = face_recognition.face_encodings(immagine1)[0]
codifica2 = face_recognition.face_encodings(immagine2)[0]

# Crea un elenco delle codifiche e dei nomi delle persone
codifiche_conosciute = [codifica1, codifica2]
nomi_conosciuti = ["Saramin", "Pera"]

# Inizializza la videocamera
videocamera = cv2.VideoCapture(0)

while True:
    # Cattura un frame dalla videocamera
    ret, frame = videocamera.read()

    # Ridimensiona il frame per migliorare le prestazioni
    piccolo_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converte l'immagine da BGR a RGB (richiesta da face_recognition)
    rgb_frame = cv2.cvtColor(piccolo_frame, cv2.COLOR_BGR2RGB)

    # Trova tutti i volti nel frame
    facce = face_recognition.face_locations(rgb_frame)
    codifiche_volto = face_recognition.face_encodings(rgb_frame, facce)

    for codifica_volto in codifiche_volto:
        # Confronta la codifica del volto con quelle conosciute
        confronti = face_recognition.compare_faces(codifiche_conosciute, codifica_volto)
        nome_riconosciuto = "Sconosciuto"

        # Trova il nome corrispondente se il volto viene riconosciuto
        if True in confronti:
            indice_corrispondenza = confronti.index(True)
            nome_riconosciuto = nomi_conosciuti[indice_corrispondenza]

            # Saluta la persona riconosciuta
            print(f"Ciao, {nome_riconosciuto}!")

        else:
            # Attiva l'allarme se il volto non viene riconosciuto
            print("Allarme attivato!")
            winsound.Beep(1000, 2000)  # Emette un suono per 2 secondi

        # Disegna un rettangolo intorno al volto e mostra il nome
        top, right, bottom, left = facce[0]
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, nome_riconosciuto, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1)

    # Mostra il frame risultante
    cv2.imshow("Riconoscimento volti", frame)

    # Interrompi l'esecuzione se viene premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
videocamera.release()
cv2.destroyAllWindows()
