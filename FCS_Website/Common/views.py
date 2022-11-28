from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import *

from authentication.models import *
from Documents.models import Document
from Wallet.models import *
from .helper import *



class Show_Doctors (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    doctors = Doctor.objects.filter (is_verified=True)
    attributes = {"data": doctors,
                  "title":"Doctors",
                  "heading":"List of all doctors"}
    return render (request, "Common/Templates/Show_Doctors.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    field = request.POST["filter_field"]
    value = request.POST["filter_value"]

    doctors = Doctor.objects.filter (is_verified=True)
    if (field == "name"):
      doctors = doctors.filter (name=value)
    elif (field == "location_district"):
      doctors = doctors.filter (location_district=value)
    elif (field == "location_state"):
      doctors = doctors.filter (location_state=value)
    elif (field == "location_country"):
      doctors = doctors.filter (location_country=value)
    elif (field == "location_pin_code"):
      doctors = doctors.filter (location_pin_code=value)

    attributes = {"data": doctors,
                  "title":"Doctors",
                  "heading":"List of all doctors"}
    return render (request, "Common/Templates/Show_Doctors.html", attributes)


def DoctorDetailView(request,pk):
  return redirect ("/login")
class InsuranceView(ListView):
  def get (self, request,pk):
    # For patients
    if( Organization.objects.filter (organization_type="Insurance", id=pk).exists()==False):
      return redirect("/login")
    if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      if (request.session.get ("authenticated", False) == False):
        return HttpResponseForbidden ()

      user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      documents = Document.objects.filter (owner_patient=user)
      return render (request, "Common/Templates/InsuranceInteract.html", {"documents":documents})

  def post(self, request,pk):

    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    document_name = request.POST.getlist ("Document")
    document = Document.objects.filter (owner_patient=user, name=document_name[0])[0]
    print(document)
    amount=request.POST.getlist ("Amount")
    patient = Patient.objects.filter(username=user.username)[0]


    try:
       org = Organization.objects.filter(organization_type="Insurance" , id=pk)[0]
       CLAIM = Insurance_Claims (document=document,firm=org,amount=amount[0],patient=patient,firm_type = "Insurance")
       CLAIM.save()
    except:
      attributes = {"title":"Claim Request Failed",
                    "heading": "Could not process claim due to some invalid entries.",
                    "redirect":"/login"}
      return render (request, "Common/Templates/message.html", attributes)
    return redirect ("/login")

class PharmacyView(ListView):
  def get (self, request,pk):
    # For patients
    if( Organization.objects.filter (organization_type="Pharmacy", id=pk).exists()==False):
      return redirect("/login")
    if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      if (request.session.get ("authenticated", False) == False):
        return HttpResponseForbidden ()

      user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      documents = Document.objects.filter (owner_patient=user)
      return render (request, "Common/Templates/PharmacyInteract.html", {"documents":documents})

  def post(self, request,pk):

    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    document_name = request.POST.getlist ("Document")
    document = Document.objects.filter (owner_patient=user, name=document_name[0])[0]
    print(document)

    patient = Patient.objects.filter(username=user.username)[0]


    try:
       org = Organization.objects.filter(organization_type="Pharmacy" , id=pk)[0]
       CLAIM = Insurance_Claims (document=document,firm=org,patient=patient, firm_type = "Pharmacy")
       CLAIM.save()
    except Exception as e:
      print(e)
      attributes = {"title":"Claim Request Failed",
                    "heading": "Could not process claim due to some invalid entries.",
                    "redirect":"/login"}
      return render (request, "Common/Templates/message.html", attributes)
    return redirect ("../../login")

class Show_Organization(ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    organization = Organization.objects.filter (is_verified=True)
    attributes = {"data": organization,
                  "title":"Organization",
                  "heading":"List of all organization"}
    return render (request, "Common/Templates/Show_Organization.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    field = request.POST["filter_field"]
    value = request.POST["filter_value"]
    typeof=request.POST["filter_type"]
    organization = Organization.objects.filter (is_verified=True)

    if(typeof!=""):
      organization = organization.filter (organization_type=typeof)

    if (field == "name"):
      organization = organization.filter (name=value)

    elif (field == "location_district"):
      organization = organization.filter (location_district=value)
    elif (field == "location_state"):
      organization = organization.filter (location_state=value)
    elif (field == "location_country"):
      organization = organization.filter (location_country=value)
    elif (field == "location_pin_code"):
      organization = organization.filter (location_pin_code=value)

    attributes = {"data": organization,
                  "title":"organization",
                  "heading":"List of all organization"}
    return render (request, "Common/Templates/Show_Organization.html", attributes)