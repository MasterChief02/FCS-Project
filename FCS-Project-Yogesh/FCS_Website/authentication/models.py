from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.base_user import BaseUserManager



class Custom_User (models.Model):
  username = models.CharField (max_length=50,unique=True)
  password = models.CharField (max_length=1024)
  name = models.CharField (max_length=50)
  email = models.EmailField (max_length=50, unique=True)
  mobile_number=models.CharField (max_length=10)
  verification_document = models.FileField (upload_to="Data/Verification",validators=[FileExtensionValidator (['pdf'])], max_length=256)
  is_verified = models.BooleanField (default=False)
  certificate_file = models.FileField (upload_to="Data/Authentication",validators=[FileExtensionValidator (['p12'])], max_length=256, blank=True)
  certificate_pass = models.CharField (max_length=20, default=BaseUserManager ().make_random_password (20))


class Patient (Custom_User):
  Type = "Patient"
  dob = models.DateField ()
  profile_picture = models.ImageField (upload_to="Data/Profile_Picture", height_field=None, width_field=None, max_length=254)
  # documents = models.ManyToManyField (Document, blank=True)

  def __str__(self):
    return self.Type + ": " + self.name

class Doctor (Custom_User):
  Type = "Doctor"
  license_number = models.CharField (max_length=10)
  location_address = models.CharField (max_length=50)
  location_district = models.CharField (max_length=50)
  location_state = models.CharField (max_length=50)
  location_country = models.CharField (max_length=50)
  location_pin_code = models.CharField (max_length=50)

  def __str__(self):
    return self.Type + ": " + self.name

class Organization (Custom_User):
  Type = "Organization"
  description = models.CharField (max_length=500)
  organization_type = models.CharField (max_length=20,
                                        choices={("Insurance","Insurance"),
                                                 ("Pharmacy", "Pharmacy"),
                                                 ("Hospital", "Hospital")
                                                },
                                        default="Hospital")
  location_address = models.CharField (max_length=50)
  location_district = models.CharField (max_length=50)
  location_state = models.CharField (max_length=50)
  location_country = models.CharField (max_length=50)
  location_pin_code = models.CharField (max_length=50)

  def __str__(self):
    return self.Type + ": " + self.organization_type + ": " + self.name

class OrganizationImage (models.Model):
  organization = models.ForeignKey (Organization, related_name='images', on_delete=models.CASCADE)
  image = models.ImageField (upload_to="Data/Profile_Picture", height_field=None, width_field=None, max_length=254)

class Keys(models.Model):
    user = models.ForeignKey(Custom_User, unique=True , on_delete=models.CASCADE)
    # username = models.ForeignKey(Custom_User, on_delete=models.CASCADE , max_length=50,unique=True)
    # username = models.CharField (max_length=50,unique=True)
    pub_key= models.CharField(max_length=1024,default=None , unique=True)
    priv_key= models.CharField(max_length=1024,default=None , unique=True)