from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.cache import cache
from django.views.generic.list import ListView
from django.core.mail import send_mail
import random

from Common.helper import *



class OTP (ListView):
  def get (self,request):
    # Checking if OTP is requested
    if (request.session.get ("otp_requested", False) == True):
      # Send email to user
      print ("Requested")
      user = get_user (request.session["username"], request.session["user_type"])
      request.session["otp"] = random.randint(100000,999999)
      print (request.session["otp"])
      recipient_list = [user.email]
      subject = "OTP for Patient Data Management Portal."
      message=f'Hello {user.name},\nYour OTP is {request.session["otp"]} '
      email_from= "group29fcswebsite@gmail.com"
      send_mail (subject,message,email_from,recipient_list)
      return render(request, "OTP/Templates/OTP.html")

    # Else redirecting to home
    else:
      return redirect(request.session.get ("otp_redirect", "/login"))



  def post(self,request):
    if(request.session["otp"].__eq__(request.POST["otp"])):
      request.session["otp_result"] =True
    else:
      request.session["otp_result"] =False
    del request.session["otp"]
    return redirect(request.session["otp_redirect"])

