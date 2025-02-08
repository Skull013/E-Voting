# Secure Voting System
Overview
---
The Secure Voting System is an application designed to ensure secure and authenticated voting using face recognition and Aadhaar number verification. This system aims to provide a digital platform for elections while ensuring voter authenticity and security.

The system works as follows:

Voter Authentication: Uses face recognition and Aadhaar number to authenticate the voter.

Voting Process: The voter selects a party to vote for after passing the authentication process.

Data Security: Votes are securely recorded with timestamps, and voter information is encrypted.

# Features
---
Face Recognition: Authenticates the voter via facial recognition technology to ensure they are eligible to vote.

Aadhaar Number Verification: Collects the Aadhaar number for added security and verification.

Voting UI: Provides a simple user interface for casting votes for different political parties.

Vote Recording: Records votes in a CSV file with timestamps.

Secure Data Storage: Voter data (such as face data and Aadhaar) is encrypted and stored securely.

Audio Feedback: Provides audio feedback to guide the voter through the process.

# Technologies Used
---
Python: The core language for the system.

OpenCV: For face detection and image processing.

Tkinter: For the graphical user interface (GUI).

Pillow: For handling images in the GUI.

KNN (K-Nearest Neighbors): For face recognition.

Fernet Encryption: For secure storage of sensitive data.

CSV: For storing votes and voter data.

Aadhaar Number Verification: Basic validation (you may later integrate with a real API for Aadhaar verification if necessary).

# Installation
---
# 1.Clone the Repository
Clone the repository to your local machine using the following command:

bash
Copy
Edit
git clone https://github.com/yourusername/Secure-Voting-System.git
2. Install Dependencies
Ensure you have Python installed. You can install the required dependencies using the following command:

nginx
Copy
Edit
pip install -r requirements.txt
3. Setting Up
Download the face recognition data (such as names.pkl and faces_data.pkl) if not included in the repo.
Place the face recognition files (secret.key, background_img.jpg, etc.) in the appropriate directories.
Ensure you have a webcam for face detection and capture.
4. Running the Application
Run the following command to start the voting system:

nginx
Copy
Edit
python SecureVoting_system.py
# Usage
---
Start Voting: Press the "Start Voting" button to begin the voting process.

Authentication:
1. After selecting a party, you will be asked to enter your Aadhaar number.
2. After Aadhaar verification, the system will attempt face recognition.

Casting Vote: Once authenticated, your vote will be recorded in a CSV file.

#Security Features
---
Encryption: All sensitive data such as Aadhaar numbers and facial features are encrypted using the Fernet encryption algorithm.

Face Recognition: The system uses a pre-trained model to compare the live feed with stored facial data to ensure the voter’s authenticity.

Secure Data Storage: All vote-related data (timestamp, vote, and voter identification) are stored in a secure and encrypted manner.

# Known Issues
---
Face recognition may fail in low-light conditions.

The Aadhaar number validation is basic and could be improved by integrating real-world API checks.

Ensure a stable internet connection for accessing libraries and face recognition training data.
# Future Enhancements
---
Integrate real-world Aadhaar validation via API.

Improve the face recognition algorithm for better accuracy and speed.

Add multi-factor authentication to enhance security.

Implement a web-based interface for wider accessibility.
# Contributing
---
We welcome contributions to improve the system! To contribute:

Fork the repository.

Create a new branch.

Implement your changes and run tests.

Submit a pull request.
# Acknowledgments
---
OpenCV for face detection and image processing.

Tkinter for building the graphical user interface.

Pillow for handling images in the GUI.

Fernet encryption for securing sensitive data.
