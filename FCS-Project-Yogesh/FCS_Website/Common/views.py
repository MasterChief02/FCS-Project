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




class Show_Organization(ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    organization = Organization.objects.filter (is_verified=True)
    attributes = {"data": organization,
                  "title":"Organization",
                  "heading":"List of all organization"}
    return render (request, "Common/Templates/Show_Organization.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False):
      return HttpResponseForbidden ()

    field = request.POST["filter_field"]
    value = request.POST["filter_value"]
    typeof=request.POST["filter_type"]
    organization = Organization.objects.filter (is_verified=True)

    if(typeof!=""):
      organization = organization.filter (organization_type=typeof)

    if (field == "name"):
      organization = organization.filter (name=value)

    elif (field == "location_district"):
      organization = organization.filter (location_district=value)
    elif (field == "location_state"):
      organization = organization.filter (location_state=value)
    elif (field == "location_country"):
      organization = organization.filter (location_country=value)
    elif (field == "location_pin_code"):
      organization = organization.filter (location_pin_code=value)

    attributes = {"data": organization,
                  "title":"organization",
                  "heading":"List of all organization"}
    return render (request, "Common/Templates/Show_Organization.html", attributes)