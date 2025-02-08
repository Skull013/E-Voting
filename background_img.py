import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
from PIL import ImageGrab

# Placeholder for registered faces (In a real-world scenario, this would be a database)
registered_faces = []  # A list of known faces (encodings) for verification

# Function to capture face and return its encoding
def capture_face_encoding():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = frame[:, :, ::-1]  # Convert from BGR to RGB
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            video_capture.release()
            cv2.destroyAllWindows()
            return face_encodings[0]  # Return the encoding of the first face detected

        # Break the loop if no face is detected
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None

# Function to simulate a vote
def submit_vote(aadhaar_number, party_choice):
    if not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
        messagebox.showerror("Invalid Aadhaar", "Please enter a valid 12-digit Aadhaar number.")
        return

    # Simulate face recognition check
    encoding = capture_face_encoding()

    if encoding:
        # Check if the face matches any known face (simulated here with registered faces)
        for known_encoding in registered_faces:
            matches = face_recognition.compare_faces([known_encoding], encoding)
            if True in matches:
                # Successful face match, submit the vote
                messagebox.showinfo("Vote Submitted", f"Your vote for {party_choice} has been successfully submitted!")
                return
        messagebox.showerror("Face Not Recognized", "Face recognition failed. Please try again.")
    else:
        messagebox.showerror("Face Detection", "No face detected. Please try again.")

# Function to take screenshot of the portal and save as PNG
def save_screenshot():
    x1 = root.winfo_rootx()
    y1 = root.winfo_rooty()
    x2 = x1 + root.winfo_width()
    y2 = y1 + root.winfo_height()

    # Capture the screenshot of the tkinter window
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Define the area to capture
    img.save("e_voting_portal.png", "PNG")
    messagebox.showinfo("Screenshot Saved", "The screenshot of the portal has been saved as e_voting_portal.png")

# Main function to create the GUI
def create_voting_portal():
    global root
    root = tk.Tk()
    root.title("E-Voting Portal")
    
    # Instructions
    label = tk.Label(root, text="Please enter your Aadhaar number and select your vote.", font=("Arial", 14))
    label.pack(pady=10)

    # Aadhaar Number Entry
    aadhaar_label = tk.Label(root, text="Enter Aadhaar Number:")
    aadhaar_label.pack(pady=5)
    aadhaar_entry = tk.Entry(root, font=("Arial", 12))
    aadhaar_entry.pack(pady=5)
    
    # Voting options
    party_label = tk.Label(root, text="Select your party:", font=("Arial", 12))
    party_label.pack(pady=10)

    party_var = tk.StringVar(value="None")
    
    # Party Buttons
    bjp_button = tk.Radiobutton(root, text="BJP", variable=party_var, value="BJP", font=("Arial", 12))
    bjp_button.pack()
    congress_button = tk.Radiobutton(root, text="Congress", variable=party_var, value="Congress", font=("Arial", 12))
    congress_button.pack()
    aap_button = tk.Radiobutton(root, text="AAP", variable=party_var, value="AAP", font=("Arial", 12))
    aap_button.pack()
    noto_button = tk.Radiobutton(root, text="NOTo", variable=party_var, value="NOTo", font=("Arial", 12))
    noto_button.pack()

    # Submit button
    submit_button = tk.Button(root, text="Submit Vote", font=("Arial", 14), command=lambda: submit_vote(aadhaar_entry.get(), party_var.get()))
    submit_button.pack(pady=20)

    # Save screenshot button
    save_button = tk.Button(root, text="Save Screenshot", font=("Arial", 12), command=save_screenshot)
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_voting_portal()
