from django.shortcuts import render,redirect

from Authentication.forms import *
from Authentication.models import *
from django.views.generic.list import ListView
from django.contrib import messages

class HomePage(ListView):
  def get(self,request):
        return render(request, "Authentication/Templates/Home.html")


class LoginPage(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/Authentication/Templates/login.html", {})
  
    if (request.session.get ("authenticated", False) == True):        
      return render(request, "Authentication/Templates/signup.html")
    else:
      return render(request, "Authentication/Templates/login.html")
  
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
        return render(request, "Authentication/Templates/"+type+".html")
    else:
        messages.warning(request, 'Invalid Username or Password.')
        return render(request, "Authentication/Templates/login.html")
      
class LogoutPage(ListView):
  def get(self,request):
        try:
            request.session["authenticated"] = False
            del request.session['username']
        except:
            return redirect('login')
        return render(request, "Authentication/Templates/signup.html")

class PatientSignup(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/Authentication/Templates/login.html", {})       
      return render(request, "Authentication/Templates/PatientSignup.html")
  
  def post(self,request):
    #user typed in credentials
    gotusername=request.POST['username']
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
  # return render(request, "FCS_Website/Authentication/Templates/login.html", {})       
      return render(request, "Authentication/Templates/DoctorSignup.html")
  
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


