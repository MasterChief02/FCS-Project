from django.views.generic.list import ListView
from django.http import HttpResponseForbidden
from django.shortcuts import render
from Documents.models import Document
from Authentication.models import *



class document_add_view (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == patient):
      return render(request, "Authentication/Templates/login.html")
    else:
      return HttpResponseForbidden ()

  def post (self, request):
    document = Document (request.POST, request.FILES)
    document.save ()



class document_share_view (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == patient):
      user = patient.objects.all ().filter (username=request.session['user'])
      attributes = {"Documents":Document.objects.all ().filter (user=user),
                    "Doctors": doctor.objects.all (),
                    "Insurance_Firms": insurance_firm.objects.all (),
                    "Pharmacies": pharmacy.objects.all (),
                    "Hospitals": hospital.objects.all (),
                   }
      return render(request, "Documents/Templates/share.html", attributes)

  def post (self, request):
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == patient):
      user = patient.objects.all ().filter (username=request.session['user'])
      document = Document.objects.all ().filter (owner_patient=user).filter (name=request.POST["doc_name"])[0]
      type = request.POST["type"]
      if (type == "Doctor"):
        document.share_with_doctor (request.POST["username"])
      elif (type == "Insurance Firm"):
        document.share_with_insurance_firm (request.POST["username"])
      elif (type == "Pharmacy"):
        document.share_with_pharmacy (request.POST["username"])
      elif (type == "Hospital"):
        document.share_with_hospital (request.POST["username"])
