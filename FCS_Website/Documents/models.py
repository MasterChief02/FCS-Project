from email.policy import default
from django.db import models
from django.core.validators import FileExtensionValidator

from Authentication.models import *


class Document (models.Model):
  document_id = models.AutoField (primary_key=True)
  name = models.CharField (max_length=100)
  file = models.FileField (validators=[FileExtensionValidator (['pdf'])])
  owner_patient = models.OneToOneField (patient, on_delete = models.CASCADE)
  shared_with_doctors = models.ManyToManyField (doctor, blank=True)
  shared_with_insurance_firm = models.ManyToManyField (insurance_firm, blank=True)
  shared_with_pharmacy = models.ManyToManyField (pharmacy, blank=True)
  shared_with_hospital = models.ManyToManyField (hospital, blank=True)


  def share_with_doctor (self, username):
    Doctor = doctor.objects.all ().filter (username=username)[0]
    self.shared_with_doctors.add (Doctor)

  def share_with_insurance_firm (self, username):
    Insurance_Firm = insurance_firm.objects.all ().filter (username=username)[0]
    self.shared_with_doctors.add (Insurance_Firm)

  def share_with_pharmacy (self, username):
    Pharmacy = pharmacy.objects.all ().filter (username=username)[0]
    self.shared_with_doctors.add (Pharmacy)

  def share_with_hospital (self, username):
    Hospital = hospital.objects.all ().filter (username=username)[0]
    self.shared_with_doctors.add (Hospital)
