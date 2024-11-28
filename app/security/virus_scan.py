import clamd
from flask import current_app
import hashlib
from cryptography.fernet import Fernet
import os

class SecurityManager:
    def __init__(self):
        self.clam = clamd.ClamdUnixSocket()
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
    def scan_file(self, file_path):
        try:
            scan_result = self.clam.scan(file_path)
            file_status = scan_result[file_path][0]
            return file_status == 'OK'
        except Exception as e:
            current_app.logger.error(f"Virus scan failed: {str(e)}")
            return False
            
    def encrypt_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            encrypted_data = self.cipher_suite.encrypt(file_data)
            
            encrypted_path = f"{file_path}.encrypted"
            with open(encrypted_path, 'wb') as file:
                file.write(encrypted_data)
                
            return encrypted_path
        except Exception as e:
            current_app.logger.error(f"File encryption failed: {str(e)}")
            return None
            
    def decrypt_file(self, encrypted_path):
        try:
            with open(encrypted_path, 'rb') as file:
                encrypted_data = file.read()
                
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return io.BytesIO(decrypted_data)
        except Exception as e:
            current_app.logger.error(f"File decryption failed: {str(e)}")
            return None
            
    @staticmethod
    def calculate_file_hash(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() 