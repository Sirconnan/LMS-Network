import random as rand
import hashlib
import os

import Crypto.Util.number as cun
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

generator = 5

def diffie_hellman_prime(): # ===> Generate the prime number for the keys
    return cun.getPrime(512)


def diffie_hellman_private_key(prime: int): # ===> Generate the private key
    return rand.randrange(2, prime - 1)


def diffie_hellman_public_key(private: int, prime: int): # ===> Generate The public key
    return pow(generator, private, prime)


def diffie_hellman_shared_key(recv_public: int, private: int, prime: int): # ===> Generte the shared key
    return pow(recv_public, private, prime)



def diffie_hellman_encrypt(message: str, shared_key: int): # ===> Encypt data whit the shared key
    message = message.encode("utf-8") # => Convert to bytes from str

    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16] # => Generate the hash key
    
    iv = os.urandom(16)  # => Generate the vector 
    cipher = AES.new(key, AES.MODE_CBC, iv) # => Setting the cipher 

    cipher_text = cipher.encrypt(pad(message, AES.block_size)) # => Encrypt data
    cipher_data = (iv + cipher_text).hex() # => Add the vector to data and convert to hexa format
    
    return cipher_data.encode("utf-8") # => Return encypt data to the bytes format



def diffie_hellman_decrypt(message:bytes, shared_key: int):  # ===> Decrypt data whit the shared key
    message = message.decode("utf-8") # => Convert to str from bytes

    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16] # => Generate the hash key
    
    cipher_data = bytes.fromhex(message) # => Convert tob bytes from hexa
    iv = cipher_data[:16] # => Extract the vector
    cipher = AES.new(key, AES.MODE_CBC, iv) # => Setting the cipher
    
    cipher_text = cipher_data[16:] # => Extract encypt data 
    message_decrypt = unpad(cipher.decrypt(cipher_text), AES.block_size) # => Decrypt data
    
    return message_decrypt.decode("utf-8") # => Return decypt data to the str format