import cv2
import face_recognition
import pyttsx3
import speech_recognition as sr
import pygame
import smtplib
import imghdr
from email.message import EmailMessage

# Carica le immagini dei volti da riconoscere
immagine_persona1 = face_recognition.load_image_file("saramin.jpg")
nome_persona1 = "Saramin"
encoding_persona1 = face_recognition.face_encodings(immagine_persona1)[0]

# Inizializza il motore text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Imposta la velocità di pronuncia

# Inizializza il riconoscimento vocale
r = sr.Recognizer()

# Inizializza la libreria pygame per la riproduzione di suoni
pygame.mixer.init()
allarme_suono = pygame.mixer.Sound("allarme.wav")

# Flag per il riconoscimento dei volti
riconoscimento_attivo = True
riconoscimento_disattivato = False

# Codice segreto per disattivare/riattivare il riconoscimento dei volti
codice_segreto = "1232"

# Configurazione delle credenziali per l'invio delle email
mittente = "tuo_indirizzo_email@gmail.com"
password = "tua_password"


# Funzione per inviare una notifica via email
def invia_notifica():
    msg = EmailMessage()
    msg['Subject'] = "Allarme: Volto non riconosciuto"
    msg['From'] = mittente
    msg['To'] = "destinatario@email.com"
    msg.set_content("Un volto non riconosciuto è stato rilevato!")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(mittente, password)
        smtp.send_message(msg)
        print("Notifica inviata.")


# Funzione per riconoscere il comando vocale
def riconosci_comando():
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        testo = r.recognize_google(audio, language="it-IT").lower()
        print("Comando riconosciuto:", testo)
        return testo
    except sr.UnknownValueError:
        print("Comando non riconosciuto.")
    except sr.RequestError as e:
        print("Errore nella richiesta:", str(e))

    return ""


# Funzione per disattivare il riconoscimento dei volti
def disattiva_riconoscimento():
    global riconoscimento_disattivato
    riconoscimento_disattivato = True
    print("Riconoscimento volti disattivato.")


# Funzione per riattivare il riconoscimento dei volti
def riattiva_riconoscimento():
    global riconoscimento_disattivato
    riconoscimento_disattivato = False
    print("Riconoscimento volti riattivato.")


# Inizializza la cattura video dalla webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Acquisisce un frame dalla webcam
    ret, frame = video_capture.read()

    if riconoscimento_attivo and not riconoscimento_disattivato:
        # Rileva i volti nel frame solo se il riconoscimento è attivo e non è disattivato
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Confronta il volto rilevato con l'immagine nota solo se il riconoscimento non è disattivato
            confronto = face_recognition.compare_faces([encoding_persona1], face_encoding)

            if confronto[0]:
                # Se il volto viene riconosciuto, emette un messaggio vocale con il nome della persona
                engine.say("Ciao, " + nome_persona1)
                engine.runAndWait()

                # Disegna un rettangolo intorno al volto e mostra il nome della persona
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, nome_persona1, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # Se il volto non viene riconosciuto, suona un allarme e invia una notifica via email
                allarme_suono.play()
                cv2.putText(frame, "Volto non riconosciuto", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                invia_notifica()
    else:
        # Se il riconoscimento dei volti è disattivato, mostra un messaggio sul frame
        cv2.putText(frame, "Riconoscimento volti disattivato", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Mostra il frame con la finestra
    cv2.imshow("Sistema di allarme", frame)

    # Riconoscimento del comando vocale per disattivare/riattivare il riconoscimento dei volti
    comando = riconosci_comando()
    if comando == "disattiva allarme " + codice_segreto:
        disattiva_riconoscimento()
    elif comando == "attiva allarme " + codice_segreto:
        riattiva_riconoscimento()

    # Esci dal loop se viene premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
video_capture.release()
cv2.destroyAllWindows()
