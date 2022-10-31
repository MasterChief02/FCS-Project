from django.shortcuts import render,redirect

from Authentication.forms import *
from Authentication.models import *
from django.views.generic.list import ListView
from django.contrib import messages

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

class PatientSingnup(ListView):
  def get(self,request):
  # return render(request, "FCS_Website/Authentication/Templates/login.html", {})
  
    if (request.session.get ("authenticated", False) == True):        
      return render(request, "Authentication/Templates/PatientSignup.html")
    else:
      return render(request, "Authentication/Templates/login.html")
  def post(self,request):
    #user typed in credentials
    pass

