from django.views.generic.list import ListView
from django.http import *
from django.shortcuts import render, redirect

from .models import Document
from authentication.models import *
from Common.helper import *



class Document_Add (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == True and request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      return render(request, "Documents/Templates/Add.html")
    else:
      return HttpResponseForbidden ()

  def post (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    name = request.POST["name"]
    file = request.POST["file"]
    try:
      document = Document (name=name, file=file, owner_patient=user)
      document.save ()
      attributes = {"title":"Document upload",
                    "heading": f"Document uploaded successfully",
                    "redirect":"/patient/dashboard"}
    except:
      attributes = {"title":"Document upload",
                    "heading": f"Document could not be uploaded",
                    "redirect":"/patient/dashboard"}
    return render (request, "Common/Templates/message.html", attributes)



class document_share_view (ListView):
  def get (self, request):
    print (request.session.get ("authenticated", None), request.session.get ("type", None))
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == "Patient"):
      user = patient.objects.all ().filter (username=request.session['user'])[0]
      attributes = {"Documents":Document.objects.filter (owner_patient=user),
                    "Doctors": doctor.objects.all (),
                    "Insurance_Firms": insurance_firm.objects.all (),
                    "Pharmacies": pharmacy.objects.all (),
                    "Hospitals": hospital.objects.all (),
                   }
      return render(request, "Documents/Templates/Share.html", attributes)
    else:
      return HttpResponseForbidden ()

  def post (self, request):
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == "Patient"):
      user = patient.objects.all ().filter (username=request.session['user'])[0]
      document = Document.objects.all ().filter (owner_patient=user).filter (name=request.POST["doc_name"])[0]
      type, username = str (request.POST["type"]).split (":")
      username = username[1:]

      document.validate ("Yogesh","key")

      if (type == "Doctor"):
        print ("Doctor", username)
        document.share_with_doctor (username)
      elif (type == "Insurance Firm"):
        print ("IF", username)
        document.share_with_insurance_firm (username)
      elif (type == "Pharmacy"):
        print ("P", username)
        document.share_with_pharmacy (username)
      elif (type == "Hospital"):
        print ("H", username)
        document.share_with_hospital (username)
      else:
        print ("H", username)
        return HttpResponseBadRequest ()
      return render(request, "Documents/Templates/Share_Success.html", {"name":username})




class document_request_verification (ListView):
  def get (self, request):
    print (request.session.get ("authenticated", None), request.session.get ("type", None))
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == "Patient"):
      user = patient.objects.all ().filter (username=request.session['user'])[0]
      attributes = {"Documents":Document.objects.filter (owner_patient=user),
                    "Doctors": doctor.objects.all (),
                    "Insurance_Firms": insurance_firm.objects.all (),
                    "Pharmacies": pharmacy.objects.all (),
                    "Hospitals": hospital.objects.all (),
                   }
      return render(request, "Documents/Templates/Share.html", attributes)
    else:
      return HttpResponseForbidden ()

  def post (self, request):
    if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == "Patient"):
      user = patient.objects.all ().filter (username=request.session['user'])[0]
      document = Document.objects.all ().filter (owner_patient=user).filter (name=request.POST["doc_name"])[0]
      type, username = str (request.POST["type"]).split (":")
      username = username[1:]

      if (type == "Doctor"):
        print ("Doctor", username)
        document.share_with_doctor (username)
      elif (type == "Insurance Firm"):
        print ("IF", username)
        document.share_with_insurance_firm (username)
      elif (type == "Pharmacy"):
        print ("P", username)
        document.share_with_pharmacy (username)
      elif (type == "Hospital"):
        print ("H", username)
        document.share_with_hospital (username)
      else:
        print ("H", username)
        return HttpResponseBadRequest ()
      return render(request, "Documents/Templates/Share_Success.html", {"name":username})



class document_show_shared (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", None) == True):
      documents = Document.objects.all ()
      if (request.session.get ("type", None) == "Patient"):
        documents = Document.objects.filter ()
      return render(request, "Documents/Templates/Doc_download.html", {"Documents":documents})

  def post (self, request):
    return Http404 ()