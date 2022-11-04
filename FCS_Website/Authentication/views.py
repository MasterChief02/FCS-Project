import random
from django.shortcuts import render,redirect

# from authentication.forms import *
from authentication.models import *
from django.views.generic.list import ListView
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
import stripe
stripe.api_key=settings.STRIPE_PRIVATE_KEY
  
class HomePage(ListView):
  def get(self,request):
        return render(request, "authentication/Templates/Home.html")


class LoginPage(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/authentication/Templates/login.html", {})
  
    if (request.session.get ("authenticated", False) == True):        
      return redirect ('Dashboard')
    else:
      return render(request, "authentication/Templates/login.html")
  
  def post(self,request):
    #user typed in credentials
    gotusername=request.POST['username']
    gotpassword = request.POST['password']
    type=request.POST['type']
    if(type.__eq__("Patient")):
      user = patient
    if(type.__eq__("Doctor")):
      user=doctor
    if(type.__eq__("Pharmacy")):
      user=pharmacy
    if(type.__eq__("Insurance_Firm")):
      user=insurance_firm
    if(type.__eq__("Hospital")):
      user=hospital
    
    User= user.objects.filter (username=gotusername)
    if (len (User) > 0 and User[0].password == gotpassword):
        request.session["authenticated"] = True
        request.session['user']=User[0].username
        request.session['type']=type
        
        
        messages.success(request, 'You are logged in successfully.')
        return redirect('Dashboard')
    else:
        messages.warning(request, 'Invalid Username or Password.')
        return render(request, "authentication/Templates/login.html")

class PaymentPage(ListView):
  
  def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['key']=settings.STRIPE_PUBLIC_KEY
        return context
      
  def get(self,request):
    if(request.session['authenticated']==True):
          pass
      # render(request,"authentication/Templates/Payment.html") 
      
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

class PharmacySignup(ListView):
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

class HospitalSignup(ListView):
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

class InsuranceFirmSignup(ListView):
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
  
class Dashboard(ListView):
  def get(self,request):
    if (request.session.get ("authenticated", False) == False):        
      return redirect('login')
    else:
      type=request.session["type"] 
      
      return render(request, "authentication/Templates/"+type+".html")
    
class otp(ListView):
  def get(self,request):
    if (request.session.get ("user", False) == False):        
      return redirect('login')
    if (request.session.get ("authenticated", False) == True):        
      return redirect('Dashboard')
    else:
      #code for emailing otp  
      username=request.session["user"]
      User=user.objects.filter(username=username)
      send_otp_for_user(User)
      return render(request, "OTP.html")
  

def send_otp_for_user(User):
  otp=random.randint(100000,999999)
  recipient_list = [User[0].email]
  subject = "OTP for verifying on Patient Data Management Portal "
  message=f'Hello {User[0].name}, this is your otp {otp} '
  email_from= "group29fcswebsite@gmail.com"
  send_mail(subject,message,email_from,recipient_list)
