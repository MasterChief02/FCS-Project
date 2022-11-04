# from email.policy import default
# from django.db import models
# from django.core.validators import FileExtensionValidator

# from authentication.models import *

# import datetime
# from cryptography.hazmat import backends
# from cryptography.hazmat.primitives.serialization import pkcs12

# from endesive.pdf import cms


# class Document (models.Model):
#   document_id = models.AutoField (primary_key=True)
#   name = models.CharField (max_length=100)
#   file = models.FileField (upload_to="Documents",validators=[FileExtensionValidator (['pdf'])], max_length=256)
#   owner_patient = models.ForeignKey (patient, on_delete = models.CASCADE)
#   shared_with_doctors = models.ManyToManyField (doctor, blank=True)
#   shared_with_insurance_firm = models.ManyToManyField (insurance_firm, blank=True)
#   shared_with_pharmacy = models.ManyToManyField (pharmacy, blank=True)
#   shared_with_hospital = models.ManyToManyField (hospital, blank=True)
#   verification_username = models.CharField (max_length=50, blank=True)
#   verification_user_type = models.CharField (max_length=50, blank=True)


#   def share_with_doctor (self, username):
#     Doctor = doctor.objects.all ().filter (username=username)[0]
#     self.shared_with_doctors.add (Doctor)

#   def share_with_insurance_firm (self, username):
#     Insurance_Firm = insurance_firm.objects.all ().filter (username=username)[0]
#     self.shared_with_doctors.add (Insurance_Firm)

#   def share_with_pharmacy (self, username):
#     Pharmacy = pharmacy.objects.all ().filter (username=username)[0]
#     self.shared_with_doctors.add (Pharmacy)

#   def share_with_hospital (self, username):
#     Hospital = hospital.objects.all ().filter (username=username)[0]
#     self.shared_with_doctors.add (Hospital)

#   def request_verification (self, username, type):
#     self.verification_username = username
#     self.verification_user_type = type

#   def validate (self, name, key):
#     date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
#     date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
#     dct = {
#         "aligned": 0,
#         "sigflagsft": 132,
#         "sigpage": 0,
#         "sigbutton": True,
#         "sigfield": "Signature1",
#         "sigandcertify": False,
#         "signaturebox": (470, 840, 570, 640),
#         "signature": "I ultimately agree",
#         "contact": name,
#         "location": "AoE",
#         "signingdate": date,
#         "reason": "No reason given",
#         "password": "1234",
#     }
#     with open("/Digi/demo-rsa2048.p12", "rb") as fp:
#       p12 = pkcs12.load_key_and_certificates(
#           fp.read(), b"demo-rsa2048", backends.default_backend()
#       )
#     print (self.file.path)
#     with open(self.file.path, "rb") as fp:
#       data = fp.read ()
#     data_signature = cms.sign(data, dct, p12[0], p12[1], p12[2], "sha256")
#     with open (self.file.path, "wb") as f:
#       f.write (data)
#       f.write (data_signature)