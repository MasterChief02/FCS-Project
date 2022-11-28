from django.db import models

from authentication.models import *
from Documents.models import Document


def approve(id):
  claim = Insurance_Claims.objects.filter(id=id)
  claim.update(system_approved=True)
  return claim[0].amount,claim[0].patient

  

class Insurance_Claims(models.Model):
  patient = models.ForeignKey (Patient, related_name='patient', on_delete=models.CASCADE)
  firm = models.ForeignKey (Organization, related_name='firm', on_delete=models.CASCADE)
  firm_type =  models.CharField (max_length=20,
                                        choices={("Insurance","Insurance"),
                                                 ("Pharmacy", "Pharmacy"),
                                                
                                                },
  )
  document = models.ForeignKey (Document, related_name='document', on_delete=models.CASCADE)
  is_approved = models.BooleanField (default=False)
  system_approved = models.BooleanField (default=False)
  amount = models.PositiveIntegerField(null = True)
  

def getar(claim) :
  
    return (claim.amount,claim.patient)

class Transactions(models.Model):
  ID = models.AutoField(primary_key=True)
  ClaimID = models.PositiveIntegerField()
  Sender = models.ForeignKey(Custom_User, related_name='Sender',on_delete=models.DO_NOTHING)
  Reciever = models.ForeignKey(Custom_User, related_name='Reciever',on_delete=models.DO_NOTHING)
  Amount = models.PositiveIntegerField()
  Success  = models.BooleanField (default=False)
  

  