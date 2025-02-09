import cv2
import pickle
import numpy as np
import os
import sqlite3
import time
import hashlib
from datetime import datetime
from win32com.client import Dispatch
from cryptography.fernet import Fernet

# Generate a secret key for encryption (Do this once and store it securely)
# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)

def load_encryption_key():
    """Load the secret key for encryption."""
    return open("secret.key", "rb").read()

def encrypt_data(data):
    """Encrypt the data using Fernet symmetric encryption."""
    fernet = Fernet(load_encryption_key())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    """Decrypt the encrypted data."""
    fernet = Fernet(load_encryption_key())
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def speak(text):
    """Text-to-speech output for feedback."""
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(text)

# Initialize Video and Face Detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ensure the data directory exists
if not os.path.exists('data/'):
    os.makedirs('data/')

# Check if names.pkl exists, if not, create it
if not os.path.exists('data/names.pkl'):
    print("names.pkl not found. Please make sure you've run the training script first.")
    exit()

with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

# Check if faces_data.pkl exists, if not, create it
if not os.path.exists('data/faces_data.pkl'):
    print("faces_data.pkl not found. Please make sure you've run the training script first.")
    exit()

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Initialize KNN Classifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# SQLite Database setup
conn = sqlite3.connect('votes.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vote TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                hash TEXT NOT NULL)''')

# Function to hash data for integrity
def hash_vote_data(name, vote, date, time):
    hash_data = f"{name}{vote}{date}{time}".encode('utf-8')
    return hashlib.sha256(hash_data).hexdigest()

# Liveness detection (Simple Example)
def is_live(frame):
    # Detect eyes as a basic check for liveness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    detected_eyes = eyes.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(detected_eyes) > 0

# Initialize Background Image
imgBackground = cv2.imread("background_img.jpg")

# Process video stream
while True:
  ret, frame = video.read()
  if not ret:
    print("Failed to capture image from camera")
    break  # Exit the loop if the frame is invalid

# Convert the frame to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Proceed with face detection and other operations
  faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    
  for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        
        # Check for liveness (basic check)
        if not is_live(frame):
            speak("Please make sure your face is visible.")
            continue
        
        # Capture timestamp
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        # Display face bounding box and name
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Encrypt the user's name
        encrypted_name = encrypt_data(output[0])

        # Store vote data in the background
        imgBackground[370:370 + 230, 255:255 + 545] = frame
        cv2.imshow('frame', imgBackground)
        
        # Check if the person has already voted (using encrypted name)
        c.execute('SELECT * FROM votes WHERE name = ?', (encrypted_name,))
        existing_vote = c.fetchone()
        
        if existing_vote:
            speak("You have already voted.")
            break
        
        # Wait for keypress for voting
        k = cv2.waitKey(1)

        if k == ord('1'):  # BJP
            vote = "BJP"
        elif k == ord('2'):  # Congress
            vote = "CONGRESS"
        elif k == ord('3'):  # AAP
            vote = "AAP"
        elif k == ord('4'):  # NOTA
            vote = "NOTA"
        else:
            continue

        # Hash the vote data
        vote_hash = hash_vote_data(encrypted_name, vote, date, timestamp)

        # Insert vote into the database with encrypted name
        c.execute('INSERT INTO votes (name, vote, date, time, hash) VALUES (?, ?, ?, ?, ?)', 
                  (encrypted_name, vote, date, timestamp, vote_hash))
        conn.commit()

        speak(f"Your vote for {vote} has been recorded.")
        time.sleep(3)  # Allow time for voice feedback
        break

video.release()
cv2.destroyAllWindows()
conn.close()
