from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os

class RSAEncryption:
    def __init__(self, key_name):
        self.private_key_path = f"{key_name}_private.pem"
        self.public_key_path = f"{key_name}_public.pem"
        self.private_key = None
        self.public_key = None

        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            self.generate_keys()
        else:
            self.load_keys()
    
    def get_public_key(self):
        return self.public_key.export_key().decode()

    def to_json(self):
        return {
            "public_key": self.get_public_key()
        }

    def generate_keys(self):
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

        with open(self.private_key_path, 'wb') as private_file:
            private_file.write(self.private_key.export_key())

        with open(self.public_key_path, 'wb') as public_file:
            public_file.write(self.public_key.export_key())

    def load_keys(self):
        with open(self.private_key_path, 'rb') as private_file:
            self.private_key = RSA.import_key(private_file.read())

        with open(self.public_key_path, 'rb') as public_file:
            self.public_key = RSA.import_key(public_file.read())

    def encrypt_message(self, message, public_key_path):
        with open(public_key_path, 'rb') as public_file:
            public_key = RSA.import_key(public_file.read())

        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message)
        return binascii.hexlify(encrypted_message)

    def decrypt_message(self, encrypted_message):
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_message = cipher.decrypt(binascii.unhexlify(encrypted_message))
        return decrypted_message
