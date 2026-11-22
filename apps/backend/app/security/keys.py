from cryptography.fernet import Fernet
from app.config import settings

def get_cipher():
    key = settings.api_key_encryption_key.encode()
    return Fernet(key)

def encrypt_key(plain_key: str) -> str:
    if not plain_key:
        return ""
    cipher = get_cipher()
    return cipher.encrypt(plain_key.encode()).decode()

def decrypt_key(encrypted_key: str) -> str:
    if not encrypted_key:
        return ""
    cipher = get_cipher()
    return cipher.decrypt(encrypted_key.encode()).decode()
