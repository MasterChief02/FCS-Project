import rsa
from cryptography.fernet import Fernet
import hashlib
import base64

def generate_keys():
    modulus_length = 1024

    (publicKey, privateKey) = rsa.newkeys(1024)

    return privateKey.save_pkcs1('PEM'), publicKey.save_pkcs1('PEM')

def encrypt_private_key(message, private_key):
  f = Fernet(bytes (private_key))
  return  f.encrypt(bytes (message))


def decrypt_public_key(encoded_encrypted_msg, private_key):
  f = Fernet(bytes (private_key))
  return f.decrypt(bytes (encoded_encrypted_msg))

def main():
  private, public = generate_keys()
  print (private)
  private = hashlib.sha512 ().hexdigest ().encode()
  private = str(base64.urlsafe_b64encode(private).decode('utf-8').replace('=','')).encode ()
  print (private)
  message = "Hello world"
  encoded = encrypt_private_key(message, private)
  print (decrypt_public_key(encoded, private))

if __name__== "__main__":
  main()