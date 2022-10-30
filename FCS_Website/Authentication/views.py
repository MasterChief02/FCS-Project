from django.shortcuts import render

from Authentication.forms import *
from Authentication.models import *



def login (request):
  # return render(request, "FCS_Website/Authentication/Templates/login.html", {})
  if (request.method == "GET"):
    if (request.session.get ("authenticated", False) == True):
      return render(request, "FCS_Website/Authentication/Templates/signup.html")
    else:
      return render(request, "FCS_Website/Authentication/Templates/login.html")
  else:
    login_form = LoginForm (request.POST)
    if login_form.is_valid ():
      Patient = patient.objects.filter (username=login_form.cleaned_data ["username"])
      if (len (Patient) > 0 and Patient[0].password == login_form.cleaned_data ["password"]):
        request.session["authenticated"] = True
        return render(request, "FCS_Website/Authentication/Templates/signup.html")
      else:
        return render(request, "FCS_Website/Authentication/Templates/login.html")
