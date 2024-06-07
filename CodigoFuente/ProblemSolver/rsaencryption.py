"""File to manage the hybrid encryption"""
import binascii
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

class RSAEncryption:
    """Class that use RSA and AES"""
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
        """Method to get the public key"""
        return self.public_key.export_key().decode()

    def to_json(self):
        """method to create a json with the public key"""
        return {
            "public_key": self.get_public_key()
        }

    def generate_keys(self):
        """Method to generate the keys"""
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

        with open(self.private_key_path, 'wb') as private_file:
            private_file.write(self.private_key.export_key())

        with open(self.public_key_path, 'wb') as public_file:
            public_file.write(self.public_key.export_key())

    def load_keys(self):
        """Method to get the keys by the path"""
        with open(self.private_key_path, 'rb') as private_file:
            self.private_key = RSA.import_key(private_file.read())

        with open(self.public_key_path, 'rb') as public_file:
            self.public_key = RSA.import_key(public_file.read())

    def encrypt_message(self, message, public_key_path):
        """Method to encrypt"""
        if isinstance(message, str):
            message = message.encode()

        with open(public_key_path, 'rb') as public_file:
            public_key = RSA.import_key(public_file.read())

        aes_key = get_random_bytes(16)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message)

        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)

        encrypted_data = {
            'aes_key': binascii.hexlify(encrypted_aes_key).decode('utf-8'),
            'nonce': binascii.hexlify(cipher_aes.nonce).decode('utf-8'),
            'tag': binascii.hexlify(tag).decode('utf-8'),
            'ciphertext': binascii.hexlify(ciphertext).decode('utf-8')
        }
        return json.dumps(encrypted_data)

    def decrypt_message(self, encrypted_message):
        """Method to Decrypt"""
        encrypted_data = json.loads(encrypted_message)
        encrypted_aes_key = binascii.unhexlify(encrypted_data['aes_key'])
        nonce = binascii.unhexlify(encrypted_data['nonce'])
        tag = binascii.unhexlify(encrypted_data['tag'])
        ciphertext = binascii.unhexlify(encrypted_data['ciphertext'])

        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return decrypted_message.decode('utf-8')
