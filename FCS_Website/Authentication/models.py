from django.db import models

# Create your models here.

class user (models.Model):
  username = models.CharField (max_length=50,unique=True)
  password = models.CharField (max_length=1024)
  name = models.CharField (max_length=50)
  email = models.EmailField (max_length=50, unique=True)
  mobile_number=models.CharField(max_length=10)
  is_verified = models.BooleanField (default=False)
  #date_added=models.DateTimeField(auto_now_add=True,null=True)

class organization (user):
  
  description = models.CharField (max_length=500)
  image_1 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_2 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_3 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_4 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_5 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
 

    
class insurance_firm(organization):
    Type="Insurance Firm"
    def __str__(self):
        return "Insurance Firm: "+self.name

class doctor(organization):

    Type="Doctor"
    license_number=models.CharField(max_length=10)
    def __str__(self):
        return "Doctor: "+self.name
    
class pharmacy(organization):   
    Type="Pharmacy"
    def __str__(self):
        return "Pharmacy: "+self.name
   
class hospital(organization):
    Type="Hospital"
    def __str__(self):
        return "Hospital: "+self.name
    
class patient (user):
  Type="Patient"
  
  #mydoctor=models.ForeignKey(doctor,null=True,on_delete=models.SET_NULL)
  #myinsurance_firm=models.ForeignKey(insurance_firm,null=True,on_delete=models.SET_NULL)
  #myhospital=models.ForeignKey(hospital,null=True,on_delete=models.SET_NULL)
  aadhar = models.CharField (max_length=20)
  dob = models.DateField ()
  id_proof = models.FileField (upload_to="Patient_ID", max_length=254)
  def __str__(self):
        return "Patient: "+self.name
      
class document(models.Model):
    owner = models.ForeignKey(patient,null=True,on_delete=models.SET_NULL)
    title=models.CharField(max_length=30)
    doc=models.FileField(upload_to='doc',blank=True)
    is_verified = models.BooleanField (default=False)
    
class pending_doctor(organization):

    Type="Unverfied Doctor"
    license_number=models.CharField(max_length=10)
    def __str__(self):
        return "Doctor: "+self.name
class pending_patient (user):
  Type="Unverfied Patient"
  aadhar = models.CharField (max_length=20)
  dob = models.DateField ()
  id_proof = models.FileField (upload_to="Patient_ID", max_length=254)
  def __str__(self):
        return "Patient: "+self.name
class pending_organization (user):
  Type="Unverfied organization"
  
  description = models.CharField (max_length=500)
  image_1 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_2 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254)
  image_3 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_4 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
  image_5 = models.ImageField (upload_to=None, height_field=None, width_field=None, max_length=254, blank=True)
    

