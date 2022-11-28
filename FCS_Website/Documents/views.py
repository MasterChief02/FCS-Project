from django.views.generic.list import ListView
from django.http import *
from django.shortcuts import render, redirect

from .models import Document
from .forms import *
from authentication.models import *
from Blockchain.models import Block, Block_Chain
from Common.helper import *
import os
from django.conf import settings


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

    form = Document_Add_Patient_form (request.POST, request.FILES)
    if not (form.is_valid ()):
      return HttpResponseBadRequest ()

    name = form.cleaned_data["name"]
    file = form.cleaned_data["file"]
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


class Request_claim(ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == True and request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      organization = Organization.objects.filter (is_verified=True)
      attributes = {"data": organization,
                  "title":"Organization",
                  "heading":"List of all organization"}
      return render(request, "Documents/Templates/Request_Claim.html", attributes)
    else:
      return HttpResponseForbidden ()


class Document_Share (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    # For patient
    if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      attributes = {"Documents":Document.objects.filter (owner_patient=user),
                    "Doctors": Doctor.objects.filter (is_verified=True),
                    "Insurance_Firms": Organization.objects.filter (is_verified=True, organization_type="Insurance"),
                    "Pharmacies": Organization.objects.filter (is_verified=True, organization_type="Pharmacy"),
                    "Hospitals": Organization.objects.filter (is_verified=True, organization_type="Hospital"),}
      return render (request, "Documents/Templates/Share_Patient.html", attributes)

    # For others
    else:
      user = get_user (request.session.get ("username", INVALID_USERNAME),
                       request.session.get ("user_type", INVALID_USER_TYPE))
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      attributes = {"Patient": Patient.objects.all (),
                    "form": Document_Share_Others_Form ()}
      return render (request, "Documents/Templates/Share_Others.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    # For patient
    if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      document_names = request.POST.getlist ("Document")
      doctor_names = request.POST.getlist ("Doctor")
      insurance_names = request.POST.getlist ("Insurance")
      hospital_name = request.POST.getlist ("Hospital")
      pharmacy_names = request.POST.getlist ("Pharmacy")
      try:
        for name in document_names:
          document = Document.objects.filter (owner_patient=user, name=name)[0]

          for d_name in doctor_names:
            document.share_with_doctor (d_name)

          for i_name in insurance_names:
            print (i_name)
            document.share_with_organization (i_name)

          for h_name in hospital_name:
            document.share_with_organization (h_name)

          for p_name in pharmacy_names:
            document.share_with_organization (p_name)

        attributes = {"title":"Document share",
                      "heading": f"Document shared successfully",
                      "redirect":"/login"}
      except:
        attributes = {"title":"Document upload",
                      "heading": f"Document could not be shared",
                      "redirect":"/document/share"}
      return render (request, "Common/Templates/message.html", attributes)

    # For others
    else:
      form = Document_Share_Others_Form (request.POST, request.FILES)
      print (form)
      if not (form.is_valid ()):
        return HttpResponseBadRequest ()

      user = get_user (form.cleaned_data["username"], "Patient")
      owner = get_user (request.session.get ("username", INVALID_USERNAME), request.session.get ("user_type", INVALID_USER_TYPE))
      if (user == None or owner == None):
        return HttpResponseBadRequest ()

      try:
        document = Document (name=form.cleaned_data["name"], file=form.cleaned_data["file"], owner_patient=user)
        document.save ()

        block = Block.create_from_data (document,request.session.get ("user_type", INVALID_USER_TYPE), 1, form.cleaned_data["private_key"])
        if (owner.private_key == form.cleaned_data["private_key"] and
            block.save (form.cleaned_data["private_key"])):
          attributes = {"title":"Document upload",
                        "heading": f"Document uploaded successfully",
                        "redirect":"/patient/dashboard"}
        else:
          attributes = {"title":"Document upload",
                      "heading": f"Document could not be uploaded",
                      "redirect":"/patient/dashboard"}
      except:
        attributes = {"title":"Document upload",
                      "heading": f"Document could not be uploaded",
                      "redirect":"/patient/dashboard"}
      return render (request, "Common/Templates/message.html", attributes)



class Document_Show (ListView):
  def get (self, request):
    # For patients
    if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
      if (request.session.get ("authenticated", False) == False):
        return HttpResponseForbidden ()

      user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      documents = Document.objects.filter (owner_patient=user)
      print (documents)
      document_list = list()
      for document in documents:
        document_list.append ((document, Block_Chain.validate (document)))
      attributes = {"documents":document_list}
      return render (request, "Documents/Templates/Show_Mine.html", attributes)

    # For others
    else:
      if (request.session.get ("authenticated", False) == False):
        return HttpResponseForbidden ()

      user = get_user (request.session.get ("username", INVALID_USERNAME),
                       request.session.get ("user_type", INVALID_USER_TYPE))

      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      if (user.Type == "Doctor"):
        documents = Document.objects.filter (shared_with_doctors=user)
      else:
        documents = Document.objects.filter (shared_with_organization=user)
      return render (request, "Documents/Templates/Show_Shared.html", {"documents":documents})



class Document_Delete (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    documents = Document.objects.filter (owner_patient=user)
    return render (request, "Documents/Templates/Delete.html", {"documents":documents})



  def post (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    name = request.POST["name"]
    try:
      Document.objects.filter (owner_patient=user, name=name).delete ()
      attributes = {"title":"Document delete",
                    "heading": f"Document deleted successfully",
                    "redirect":"/login"}
    except:
      attributes = {"title":"Document delete",
                    "heading": f"Document could not be deleted",
                    "redirect":"/document/delete"}
    return render (request, "Common/Templates/message.html", attributes)



class Document_Sign (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    documents = Document.objects.filter (owner_patient=user)
    document_list = list ()
    for document in documents:
      if not (Block_Chain.validate (document)):
        document_list.append (document)
    return render (request, "Documents/Templates/Sign.html", {"documents":document_list})



  def post (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    document_id = request.POST["document_id"]
    private_key = request.POST["private_key"]
    # try:
    document = Document.objects.filter (owner_patient=user, document_id=document_id)[0]
    if (Block_Chain.digital_sign (document, "Patient", request.session.get ("username", INVALID_USERNAME), private_key) and
        private_key == str (user.private_key)):
      attributes = {"title":"Document sign",
                    "heading": f"Document signed successfully",
                    "redirect":"/login"}
    else:
      print ("unsigned")
      attributes = {"title":"Document sign",
                  "heading": f"Document could not be signed",
                  "redirect":"/document/sign"}
    # except:
    #   attributes = {"title":"Document sign",
    #                 "heading": f"Document could not be sign",
    #                 "redirect":"/document/sign"}
    return render (request, "Common/Templates/message.html", attributes)

def viewpdf(request , pk):
  if (request.session.get ("authenticated", False) == False):
    return HttpResponseForbidden ()
  document = Document.objects.filter(document_id = pk)[0]
  doc = str (document.file.url).split ("/")[-1]
  #Project\FCS_Website\media\Documents\19-20_DxSNTtA.pdf
  #doc = "19-20_nWnRSqG.pdf"
  root = settings.MEDIA_ROOT + "\Documents"
  my_file =os.path.join(root, doc)
  return HttpResponse(open(my_file, 'rb'), content_type='application/pdf')