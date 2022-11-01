from django.views.generic.list import ListView
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from Documents.models import Document
from authentication.models import *



class document_add_view (ListView):
  def get (self, request):
    # if (request.session.get ("authenticated", None) == True and request.session.get ("type", None) == patient):
      return render(request, "Documents/Templates/Add.html")
    # else:
    #   return HttpResponseForbidden ()

  def post (self, request):
    document = Document (request.POST, request.FILES)
    document.save ()



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