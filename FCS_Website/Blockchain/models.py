from django.db import models

from authentication.models import *
from Common.helper import *
from Common.crypto import PKI
from Documents.models import Document

import hashlib
import json
import time

# Create your models here.
class Block_Chain (models.Model):
  block_id = models.AutoField (primary_key=True)
  block = models.CharField (max_length=50000)


  # @staticmethod
  # def get_block_for_user_document ()

  @staticmethod
  def get_last_hash ():
    block_chain = Block_Chain.objects.all ()
    if (len (block_chain) == 0):
      return ""
    last_block = block_chain[len (block_chain) - 1]
    return hashlib.sha512 (last_block.block.encode ("UTF-8")).hexdigest ()

  @staticmethod
  def create_block (document:Document,
                    user_name:str,
                    private_key:str):
    # document = Document.objects.all ()[0]
    block = Block.create_from_data (document, "patient", user_name, private_key)
    print (block.get_json_string (""))
    block.save (private_key)
    length = len (Block_Chain.objects.all ())
    block = Block_Chain.objects.all ()[length-1]
    block = Block.create_from_string (block.block)
    print (block.get_json_string (""))
    print (block.validate ())

  @staticmethod
  def digital_sign (document:Document,
                    user_type:str,
                    user_name:str,
                    private_key:str):
    block = Block.create_from_data (document, user_type, user_name, private_key)
    if block.validate ():
      block.save (private_key)
      return True
    return False

  @staticmethod
  def validate (document:Document):
    block_chain = Block_Chain.objects.all ()
    print ("validate")
    for _block in block_chain:
      block = Block.create_from_string (_block.block)
      if ((block.validate ()) and
          (int (block.document_id) == int (document.document_id))):
        document_hash = document.get_hash ()
        if (document_hash == block.document_hash):
          print (block.document_id, document.document_id)
          print (block.document_hash)
          print (document_hash)
          print (block.validate (), (int (block.document_id) == int (document.document_id)), (block.document_hash == document_hash))
          return True
    return False


class Block ():
  def __init__(self) -> None:
    self.document:Document = None

    # Data in the encrypted block
    self.document_id:int        = 0
    self.document_hash:str      = ""
    self.encrypted_content:str  = ""
    self.decrypted_content:dict = {}

    # Data outside the encrypted block
    self.prev_hash:str    = ""
    self.timestamp:str    = ""
    self.content_hash:str = ""
    self.nonce:str        = ""
    self.user_type:str    = ""
    self.user_name:str    = ""
    self.next_block:int   = 0

  @staticmethod
  def create_from_data (document:Document,
                        user_type:str,
                        user_name:str,
                        private_key:str):
    self = Block ()
    self.document:Document = document

    # Data in the encrypted block
    self.document_id           = document.document_id
    self.document_hash         = document.get_hash ()
    self.decrypted_content     = {"document_id": self.document_id,
                                  "document_hash": self.document_hash}
    print (self.document_hash)
    content                    = json.dumps (self.decrypted_content)
    self.encrypted_content:str = PKI.encrypt_private_key (content, private_key)

    # Data outside the encrypted block
    self.prev_hash:str    = Block_Chain.get_last_hash ()
    self.timestamp:str    = str (time.time ())
    self.content_hash:str = hashlib.sha512 (self.encrypted_content.encode ("UTF-8")).hexdigest ()
    self.nonce:str        = self.find_nonce ()
    self.user_type:str    = user_type
    self.user_name:str    = user_name
    self.next_block:int   = 0

    return self


  @staticmethod
  def create_from_string (string:str):
    self = Block ()
    data = json.loads (string)

    # Data outside the encrypted block
    self.prev_hash:str    = data.get ("prev_hash", "")
    self.timestamp:str    = data.get ("timestamp", "")
    self.content_hash:str = data.get ("content_hash", "")
    self.nonce:str        = data.get ("nonce", "")
    self.user_type:str    = data.get ("user_type", "")
    self.user_name:str    = data.get ("user_name", "")
    self.next_block:int   = int (data.get ("next_block", ""))

    # Obtain public key and decrypting content
    public_key = ""
    # Data outside the encrypted block
    self.encrypted_content = json.loads (data.get ("encrypted_content", ""))
    self.decrypted_content = PKI.decrypt_public_key (self.encrypted_content, public_key)
    self.document_id = int (self.decrypted_content.get ("document_id", 0))
    self.document_hash = self.decrypted_content.get ("document_hash", "")

    return self


  def get_json_string (self, private_key):
    data_json = {"encrypted_content": self.encrypted_content,
                 "prev_hash": self.prev_hash,
                 "timestamp": self.timestamp,
                 "content_hash": self.content_hash,
                 "nonce": self.nonce,
                 "user_type": self.user_type,
                 "user_name": self.user_name,
                 "next_block": self.next_block}
    return json.dumps (data_json)


  def save (self, private_key):
    block_data = self.get_json_string (private_key)
    block = Block_Chain (block=block_data)
    if self.validate ():
      block.save ()
      return True
    return False


  def validate (self):
    data = str (self.prev_hash + str (self.timestamp)+ self.content_hash + str (self.nonce)).encode ("UTF-8")
    data_hash = hashlib.sha512 (data).hexdigest ().encode ("UTF-8")
    start_n_bytes = str (bytes (data_hash))[2:4]
    if (start_n_bytes == "00"):
      return True
    return False


  def find_nonce (self):
    self.nonce = 0
    while (True):
      if (self.validate ()):
        return str (self.nonce)
      self.nonce += 1