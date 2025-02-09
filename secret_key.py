from cryptography.fernet import Fernet

# Generate the key
key = Fernet.generate_key()

# Save the key to a file named 'secret.key'
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("Encryption key 'secret.key' has been created!")