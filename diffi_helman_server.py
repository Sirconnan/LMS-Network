import random as rand
import hashlib

import Crypto.Util.number as cun
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

generator = 5

def diffie_hellman_prime():
    return cun.getPrime(512)

def diffie_hellman_private_key(prime):
    return rand.randrange(2, prime - 1)

def diffie_hellman_public_key(private, prime):
    return pow(generator, private, prime)

def diffie_hellman_shared_key(recv_public, private, prime):
    return pow(recv_public, private, prime)

def diffie_hellman_encrypt(message: bytes, shared_key):
    iv = b'sJh\x93\x1b\xda\x9c\xbf\x886\x86tl\xa2\x9c\xfe'
    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(message, AES.block_size))
    cipher_data = (iv + cipher_text).hex()
    return cipher_data

def diffie_hellman_decrypt(message: bytes, shared_key):
    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16]
    cipher_data = bytes.fromhex(message)
    iv = cipher_data[:16]
    cipher_text = cipher_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message_decrypt = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return message_decrypt
