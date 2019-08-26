import base64
import logging
from random import SystemRandom

from cryptography.exceptions import AlreadyFinalized
from cryptography.exceptions import InvalidTag
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# def encrypt(clear,key):
#     enc = []
#     for i in range(len(clear)):
#         key_c = key[i % len(key)]
#         enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
#         enc.append(enc_c)
#     return base64.urlsafe_b64encode("".join(enc).encode()).decode()

# def decrypt(enc,key):
#     dec = []
#     enc = base64.urlsafe_b64decode(enc).decode()
#     for i in range(len(enc)):
#         key_c = key[i % len(key)]
#         dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
#         dec.append(dec_c)
#     return "".join(dec)

def encrypt(clear,key,salt,nonce):
    password_bytes = key.encode('utf-8')
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA512(),
    length=32,
    salt=salt,
    iterations=10000,
    backend=default_backend()
    )
    key = kdf.derive(password_bytes)
    aesgcm = AESGCM(key)
    cipher_text_bytes = aesgcm.encrypt(
        nonce=nonce,
        data=clear.encode('utf-8'),
        associated_data=None
        )
    cipher_text = base64.urlsafe_b64encode(cipher_text_bytes)
    return cipher_text

def decrypt(enc,key,salt,nonce):
    password_bytes = key.encode('utf-8')
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA512(),
    length=32,
    salt=salt,
    iterations=10000,
    backend=default_backend()
    )
    key = kdf.derive(password_bytes)
    aesgcm = AESGCM(key)
    decrypted_cipher_text_bytes = aesgcm.decrypt(
        nonce=nonce,
        data=base64.urlsafe_b64decode(enc),
        associated_data=None
    )
    decrypted_cipher_text = decrypted_cipher_text_bytes.decode('utf-8')
    return decrypted_cipher_text
