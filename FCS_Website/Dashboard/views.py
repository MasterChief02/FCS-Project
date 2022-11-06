from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import *

from Common.helper import *



class Dashboard_Patient (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Dashboard_Patient.html", attributes)



  def post (self, request):
    return HttpResponseBadRequest ()



class Edit_Patient (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Edit_Patient.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    dob = request.POST['dob']
    try:
      Patient.objects.filter (username=user.username).update (name=name, email=email)
      attributes = {"title":"Information update",
                    "heading": f"Information updated successfully for {name}",
                    "redirect":"/patient/dashboard"}
    except:
      attributes = {"title":"Information update",
                    "heading": f"Information could not be updated for {name}",
                    "redirect":"/patient/edit"}
    return render (request, "Common/Templates/message.html", attributes)


