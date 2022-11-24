from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import *

from authentication.models import *
from .helper import *



class Show_Doctors (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    doctors = Doctor.objects.filter (is_verified=True)
    attributes = {"data": doctors,
                  "title":"Doctors",
                  "heading":"List of all doctors"}
    return render (request, "Common/Templates/Show_Doctors.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    field = request.POST["filter_field"]
    value = request.POST["filter_value"]

    doctors = Doctor.objects.filter (is_verified=True)
    if (field == "name"):
      doctors = doctors.filter (name=value)
    elif (field == "location_district"):
      doctors = doctors.filter (location_district=value)
    elif (field == "location_state"):
      doctors = doctors.filter (location_state=value)
    elif (field == "location_country"):
      doctors = doctors.filter (location_country=value)
    elif (field == "location_pin_code"):
      doctors = doctors.filter (location_pin_code=value)

    attributes = {"data": doctors,
                  "title":"Doctors",
                  "heading":"List of all doctors"}
    return render (request, "Common/Templates/Show_Doctors.html", attributes)



