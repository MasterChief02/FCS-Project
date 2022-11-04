import random
from django.shortcuts import render,redirect

from authentication.forms import *
from authentication.models import *
from django.views.generic.list import ListView
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
import stripe
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'



class LoginPage (ListView):
  def get(self,request):
    if (request.session.get ("authenticated", False) == True):
      return redirect (f"{request.session['type']}/Dashboard")
    else:
      return render (request, "authentication/Templates/login.html")

  def post(self,request):
    username=request.POST['username']
    password = request.POST['password']
    type=request.POST['type']
    if(type.__eq__("Patient")):
      user = Patient
    if(type.__eq__("Doctor")):
      user = Doctor
    if(type.__eq__("Organization")):
      user = Organization

    User= user.objects.filter (username=username)
    if (len (User) > 0 and User[0].password == password):
        request.session["authenticated"] = False
        print (request.session["authenticated"])
        request.session['user']=User[0].username
        request.session['type']=type
        return redirect('otp')
    else:
        request.session["authenticated"] = False
        print (request.session["authenticated"])
        messages.warning(request, 'Invalid Username or Password.')
        return render(request, "authentication/Templates/login.html")

# class PaymentPage(ListView):

#   def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['key']=settings.STRIPE_PUBLIC_KEY
#         return context

#   def get(self,request):
#     if(request.session['authenticated']==True):
#           pass
#       # render(request,"authentication/Templates/Payment.html")

class LogoutPage(ListView):
  def get(self,request):
        try:
            request.session["authenticated"] = False
            del request.session['username']
        except:
            return redirect("/")
        return render(request, "authentication/Templates/signup.html")

class PatientSignup(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/authentication/Templates/login.html", {})
      return render(request, "authentication/Templates/PatientSignup.html")

  def post(self,request):
    #user typed in credentials
    gotusername=request.POST['username']
    User= user.objects.filter (username=gotusername).exists()
    if(User):
      messages.warning(request,'Username already taken')
      return redirect('signup')
    email=request.POST['email']
    name=request.POST['name']
    password = request.POST['password']
    repassword = request.POST['repassword']
    if((password.__eq__(repassword))==False):
      messages.warning(request,'Enter same password')
      return redirect('signup')

    Aadhar=request.POST['Aadhar']
    mobile_number=request.POST['mobile_number']
    identity_proof=request.POST['identity_proof']
    dob=request.POST['dob']
    add_patient = patient(username=gotusername, password=password,email=email,name=name,aadhar=Aadhar,mobile_number=mobile_number,dob=dob,id_proof=identity_proof)
    add_patient.save()
    return redirect('login')

class DoctorSignup(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/authentication/Templates/login.html", {})
      return render(request, "authentication/Templates/DoctorSignup.html")

  def post(self,request):
    #user typed in credentials
    gotusername=request.POST['username']
    User= user.objects.filter (username=gotusername).exists()
    if(User):
      messages.warning(request,'Username already taken')
      return redirect('signup')
    email=request.POST['email']
    name=request.POST['name']
    password = request.POST['password']
    repassword = request.POST['repassword']
    if((password.__eq__(repassword))==False):
      messages.warning(request,'Enter same password')
      return redirect('DoctorSignup')


    mobile_number=request.POST['mobile_number']
    license_number=request.POST['license']
    User= doctor.objects.filter (license_number=license_number).exists()
    if(User):
      messages.warning(request,'license_number already registered')
      return redirect('DoctorSignup')
    add_doctor = doctor(username=gotusername, password=password,email=email,name=name,mobile_number=mobile_number,license_number=license_number)
    add_doctor.save()
    return redirect('login')

class OrganizationSignup(ListView):
  def get(self,request):
      # return render(request, "FCS_Website/authentication/Templates/login.html", {})
      return render(request, "authentication/Templates/OrganizationSignup.html")

  def post(self,request):
    #user typed in credentials
    gotusername=request.POST['username']

    User= user.objects.filter (username=gotusername).exists()
    if(User):
      messages.warning(request,'Username already taken')
      return redirect('signup')
    email=request.POST['email']
    name=request.POST['name']
    password = request.POST['password']
    repassword = request.POST['repassword']
    if((password.__eq__(repassword))==False):
      messages.warning(request,'Enter same password')
      return redirect('DoctorSignup')


    mobile_number=request.POST['mobile_number']
    description=request.POST['description']
    Image1=request.POST['Image1']
    Image2=request.POST['Image2']
    type=request.POST['type']
    if(type.__eq__("Pharmacy")):
      user=pharmacy
    if(type.__eq__("Insurance_Firm")):
      user=insurance_firm
    if(type.__eq__("Hospital")):
      user=hospital

    add_user = user(username=gotusername, password=password,email=email,name=name,mobile_number=mobile_number,description=description,image_1=Image1,image_2=Image2)
    add_user.save()
    return redirect('login')



class Dashboard(ListView):
  def get(self,request):
    if (request.session.get ("authenticated", False) == False):
      return redirect('login')
    else:
      type=request.session["type"]

      return render(request, "authentication/Templates/"+type+".html")

class otp(ListView):
  def get(self,request):
    messages.success(request, "Message sent." )
    if (request.session.get ("user", False) == False):
      return redirect('login')
    if (request.session.get ("authenticated", False) == True):
      return redirect('Dashboard')
    else:
      #code for emailing otp

      username=request.session["user"]
      User=user.objects.filter(username=username)
      if(cache.get(User[0].email)):
        messages.warning(request, "OTP already sent")
        return render(request,'authentication/Templates/OTP.html')
      otp=random.randint(100000,999999)
      request.session["otp"] =otp
      cache.set(User[0].email,otp,timeout=100)
      send_otp_for_user(otp,User)
      return render(request, "authentication/Templates/OTP.html")
  def post(self,request):
    otp_recieved=request.POST["otp"]
    if(request.session["otp"].__eq__(otp_recieved)):
      request.session["authenticated"] =True
      return redirect('Dashboard')
    else:
      return redirect('login')


def send_otp_for_user(otp,User):

  recipient_list = [User[0].email]

  subject = "OTP for verifying on Patient Data Management Portal "
  message=f'Hello {User[0].name}, this is your otp {otp} '
  email_from= "group29fcswebsite@gmail.com"
  send_mail(subject,message,email_from,recipient_list)



class Signup(ListView):
  def get(self,request):
      # return render(request, "FCS_Website/authentication/Templates/login.html", {})
      return render(request, "authentication/Templates/Signup.html")