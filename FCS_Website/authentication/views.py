from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.http import *
import hashlib

from authentication.models import *
from Common.helper import *
from Common.crypto import *



class LoginPage (ListView):
  def get (self,request):
    redirected_from_otp = (request.session.get ("authenticated", False) == False and
                           request.session.get ("otp_requested", False) == True and
                           request.session.get ("otp_result", False) == True)
    logged_in = request.session.get ("authenticated", False) == True
    print (request.session.get ("otp_result", "Failed"))

    if (logged_in or redirected_from_otp):
      if "otp_requested" in request.session.keys ():
        del request.session["otp_requested"]
      if "otp_result" in request.session.keys ():
        del request.session["otp_result"]
      if "otp_redirect" in request.session.keys ():
        del request.session["otp_redirect"]

      user = get_user (request.session.get ("username", INVALID_USERNAME),
                       request.session.get ("user_type", INVALID_USER_TYPE))

      if (user == None):
        request.session["authenticated"] = False
        return redirect ("/login")

      request.session["authenticated"] = True
      if (request.session.get ("user_type", INVALID_USER_TYPE) == "Patient"):
        return redirect (f"/patient/dashboard")
      elif (request.session.get ("user_type", INVALID_USER_TYPE) == "Doctor"):
        return redirect (f"/doctor/dashboard")
      elif (request.session.get ("user_type", INVALID_USER_TYPE) == "Organization"):
        if (user.organization_type == "Hospital"):
          return redirect (f"/hospital/dashboard")
        elif (user.organization_type == "Pharmacy"):
          return redirect (f"/pharmacy/dashboard")
        elif (user.organization_type == "Insurance"):
          return redirect (f"/insurance/dashboard")

    else:
      return render (request, "authentication/Templates/login.html")



  def post (self,request):
    print ("Origin", request.META.get('HTTP_REFERER'))
    username = request.POST['username']
    password = hashlib.sha512 (request.POST['password'].encode ()).hexdigest ()
    type=request.POST['type']

    user = get_user (username, type)
    if (user==None):
      return render (request, "Common/Templates/message.html", {"title":"Login Failed", "heading": "Invalid username, password or type", "redirect":"/login"})

    if (user.password == password):
      request.session["authenticated"] = False
      request.session["username"] = user.username
      request.session["user_type"] = type
      request.session["otp_requested"] = True
      request.session["otp_result"] = False
      request.session["otp_redirect"] = "/login"
      print ("Redirect")
      return redirect ('/otp')
    else:
      request.session["authenticated"] = False
      return render (request, "Common/Templates/message.html", {"title":"Login Failed", "heading": "Invalid username, password or type", "redirect":"/login"})



class LogoutPage (ListView):
  def get (self, request):
    if "username" in request.session.keys ():
      del request.session["username"]
    if "user_type" in request.session.keys ():
      del request.session["user_type"]
    if "authenticated" in request.session.keys ():
      del request.session["authenticated"]
    return render (request, "Common/Templates/message.html", {"title":"Logout","heading": "Logout successfully", "redirect":"/"})



  def post (self, request):
    return HttpResponseBadRequest ()



class Signup_Patient (ListView):
  def get (self, request):
    return render (request, "authentication/Templates/Signup_Patient.html")

  def post (self, request):
    # Retrieving data
    username = request.POST['username']
    password = hashlib.sha512 (request.POST['password'].encode ()).hexdigest ()
    re_password = hashlib.sha512 (request.POST['re_password'].encode ()).hexdigest ()
    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    identity_proof = request.POST['identity_proof']
    dob = request.POST['dob']
    profile_picture = request.POST['profile_picture']

    # Check username already taken
    if (get_user (username, "Patient") != None):
      attributes = {"title":"Signup Failed",
                    "heading": "Username already taken",
                    "redirect":"/signup/patient"}
      return render (request, "Common/Templates/message.html", attributes)

    # Check passwords are not equal
    if not (password.__eq__ (re_password)):
      attributes = {"title":"Signup Failed",
                    "heading": "Passwords do not match",
                    "redirect":"/signup/patient"}
      return render (request, "Common/Templates/message.html", attributes)

    # Add patient
    try:
      private_key , public_key = PKI.create_key_pair ()
      user = Patient (username=username,
                      password=password,
                      name=name,
                      email=email,
                      mobile_number=mobile_number,
                      verification_document=identity_proof,
                      dob=dob,
                      profile_picture=profile_picture,
                      public_key=public_key,
                      private_key=private_key)
      user.save()

      attributes = {"title":"Signup Successful",
                    "heading": f"Account created successfully for {name} with private key: {private_key}",
                    "redirect":"/login",
                    "time":20}
      return render (request, "Common/Templates/message.html", attributes)

    except:
      attributes = {"title":"Signup Failed",
                    "heading": "Could not create account due to some invalid entries.",
                    "redirect":"/signup/patient"}
      return render (request, "Common/Templates/message.html", attributes)



class Signup_Doctor (ListView):
  def get (self, request):
    return render(request, "authentication/Templates/Signup_Doctor.html")



  def post (self, request):
    # Retrieving data
    username = request.POST['username']
    password = hashlib.sha512 (request.POST['password'].encode ()).hexdigest ()
    re_password = hashlib.sha512 (request.POST['re_password'].encode ()).hexdigest ()
    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    identity_proof = request.POST['identity_proof']
    license_number = request.POST['license_number']
    location_address = request.POST['location_address']
    location_district = request.POST['location_district']
    location_state = request.POST['location_state']
    location_country = request.POST['location_country']
    location_pin_code = request.POST['location_pin_code']

    # Check username already taken
    if (get_user (username, "Patient") != None):
      attributes = {"title":"Signup Failed",
                    "heading": "Username already taken",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)

    # Check passwords are not equal
    if not (password.__eq__ (re_password)):
      attributes = {"title":"Signup Failed",
                    "heading": "Passwords do not match",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)

    # Add patient
    try:
      private_key , public_key = PKI.create_key_pair ()
      user = Doctor (username=username,
                      password=password,
                      name=name,
                      email=email,
                      mobile_number=mobile_number,
                      verification_document=identity_proof,
                      license_number=license_number,
                      location_address=location_address,
                      location_district=location_district,
                      location_state=location_state,
                      location_country=location_country,
                      location_pin_code=location_pin_code,
                      public_key=public_key,
                      private_key=private_key)

      user.save()
      attributes = {"title":"Signup Successful",
                    "heading": f"Account created successfully for {name} with private key: {private_key}",
                    "redirect":"/login",
                    "time":20}
      return render (request, "Common/Templates/message.html", attributes)

    except:
      attributes = {"title":"Signup Failed",
                    "heading": "Could not create account due to some invalid entries.",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)



class Signup_Organization (ListView):
  def get (self, request):
    return render(request, "authentication/Templates/Signup_Organization.html")



  def post (self, request):
    print (request.POST)
    # Retrieving data
    username = request.POST['username']
    password = hashlib.sha512 (request.POST['password'].encode ()).hexdigest ()
    re_password = hashlib.sha512 (request.POST['re_password'].encode ()).hexdigest ()
    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    identity_proof = request.POST['identity_proof']
    description = request.POST['description']
    organization_type = request.POST['organization_type']
    location_address = request.POST['location_address']
    location_district = request.POST['location_district']
    location_state = request.POST['location_state']
    location_country = request.POST['location_country']
    location_pin_code = request.POST['location_pin_code']

    # Check username already taken
    if (get_user (username, "Patient") != None):
      attributes = {"title":"Signup Failed",
                    "heading": "Username already taken",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)

    # Check passwords are not equal
    if not (password.__eq__ (re_password)):
      attributes = {"title":"Signup Failed",
                    "heading": "Passwords do not match",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)

    # Add patient
    try:
      private_key , public_key = PKI.create_key_pair ()
      user = Organization (username=username,
                      password=password,
                      name=name,
                      email=email,
                      mobile_number=mobile_number,
                      verification_document=identity_proof,
                      description=description,
                      organization_type=organization_type,
                      location_address=location_address,
                      location_district=location_district,
                      location_state=location_state,
                      location_country=location_country,
                      public_key=public_key,
                      private_key=private_key)

      user.save()
      attributes = {"title":"Signup Successful",
                    "heading": f"Account created successfully for {name} with private key: {private_key}",
                    "redirect":"/login",
                    "time":20}
      return render (request, "Common/Templates/message.html", attributes)

    except:
      attributes = {"title":"Signup Failed",
                    "heading": "Could not create account due to some invalid entries.",
                    "redirect":"/signup/doctor"}
      return render (request, "Common/Templates/message.html", attributes)
