import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from decouple import config

# Clave para Cifrar, 24 caracteres = 192 Bits
SECRET_KEY = (config('SECRET_KEY')).encode('utf-8')


# Función para cifrar la connection string usando AES en modo CBC
def encrypt_string(connection_string: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Revisar el padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(connection_string.encode()) + padder.finalize()

    # Cifrar los datos
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Codificar en Base64 para almacenar como string
    return base64.b64encode(iv + encrypted).decode()


# Función para descifrar la connection string
def decrypt_string(encrypted_string: str) -> str:
    encrypted_data = base64.b64decode(encrypted_string)
    iv = encrypted_data[:16]
    encrypted = encrypted_data[16:]

    # Crear un descifrador AES en modo CBC
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Descifrar los datos
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

    # Remover el padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted.decode()