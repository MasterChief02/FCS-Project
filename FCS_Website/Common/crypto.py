import rsa

class PKI ():
  @staticmethod
  def create_key_pair ():
    publicKey, privateKey = rsa.newkeys (1024)
    return privateKey.save_pkcs1 ('PEM'), publicKey.save_pkcs1 ('PEM')

  @staticmethod
  def encrypt_public_key (message, public_key):
    return message

  @staticmethod
  def decrypt_private_key (message, private_key):
    return message

  @staticmethod
  def encrypt_private_key (message, private_key):
    return message

  @staticmethod
  def decrypt_public_key (message, public_key):
    return message

