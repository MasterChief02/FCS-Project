from django.db import models



class user (models.Model):
  username = models.CharField (max_length=50)
  password = models.CharField (max_length=1024)
  email = models.EmailField (max_length=50)
  is_verified = models.BooleanField (default=False)



class patient (user):
  # name = models.CharField (max_length=50)
  aadhar = models.CharField (max_length=20)
  mobile_number = models.CharField (max_length=10)
  dob = models.DateField ()
  # id_proof = models.FileField (upload_to=None, max_length=254)




class organization (user):
  name = models.CharField (max_length=100)
  description = models.CharField (max_length=500)
  image_1 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_2 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_3 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_4 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_5 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)