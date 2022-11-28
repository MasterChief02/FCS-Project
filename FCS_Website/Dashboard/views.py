from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import *
from Wallet.models import *
from Common.helper import *

# for / page startup function
class Startup(ListView):
    def get (self, request):
      return render (request, "Dashboard/Templates/Startup.html")


class Dashboard_Patient (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    user = Patient.objects.filter (username=user.username)[0]
    unaproved = Insurance_Claims.objects.filter(patient=user,is_approved=True, system_approved = False,firm_type="Pharmacy" )

    attributes = {"user":user,"unapproved":unaproved}

    return render (request, "Dashboard/Templates/Dashboard_Patient.html", attributes)



  def post (self, request):
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Patient"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Patient")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")


    claims = request.POST.getlist ("claim")[0]
    claims=int(claims)
    claim = Insurance_Claims.objects.filter(id=claims)[0]
    request.session["claimID"] = claims
    AMOUNT = claim.amount
    reciever = claim.firm

    try:
      transaction = Transactions(ClaimID =claims, Sender=user,Reciever = reciever , Amount = AMOUNT)
      transaction.save()
      request.session["transaction"] = transaction.ID
      return redirect('payment')

    except:
      attributes = {"title":"Transaction",
                    "heading": "Something wrong with parameters",
                    "redirect":"login"}
      return render (request, "Common/Templates/message.html", attributes)


class Dashboard_Doctor (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Doctor"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Doctor")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Dashboard_Doctor.html", attributes)



  def post (self, request):
    return HttpResponseBadRequest ()


class Dashboard_Pharmacy (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Organization"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    if(typeof.__eq__("Pharmacy")==False):
      return HttpResponseForbidden ()

    insure = Organization.objects.filter (organization_type="Pharmacy", username=user.username)[0]
    unaproved = Insurance_Claims.objects.filter(firm=insure,is_approved=False , system_approved = False)
    approvedclaims= Insurance_Claims.objects.filter(firm=insure , is_approved=True,system_approved = True)
    incomplete = Insurance_Claims.objects.filter(firm=insure,is_approved=True, system_approved = False)
    attributes = {"user":user,"unapproved":unaproved,"approved":approvedclaims , 'incomplete':incomplete}


    return render (request, "Dashboard/Templates/Dashboard_Pharmacy.html", attributes)



  def post (self, request):
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Organization"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    if(typeof.__eq__("Pharmacy")==False):
      return HttpResponseForbidden ()

    claims = request.POST.getlist ("claim")[0]
    Amount = request.POST.getlist ("Amount")[0]
    claims=int(claims)
    claim = Insurance_Claims.objects.filter(id=claims)
    claim.update(amount=Amount , is_approved = True)
    claim = claim[0]

    return redirect('login')



class Dashboard_Insurance (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Organization"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    if(typeof.__eq__("Insurance")==False):
      return HttpResponseForbidden ()

    insure = Organization.objects.filter (organization_type="Insurance", username=user.username)[0]
    approvedclaims= Insurance_Claims.objects.filter(firm=insure , is_approved=True ,system_approved = True)
    unaproved = Insurance_Claims.objects.filter(firm=insure,system_approved = False)
    attributes = {"user":user,"approved":approvedclaims ,"unapproved":unaproved }

    return render (request, "Dashboard/Templates/Dashboard_Insurance.html", attributes)

  def post (self, request):
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Organization"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    if(typeof.__eq__("Insurance")==False):
      return HttpResponseForbidden ()
    claims = request.POST.getlist ("claim")[0]
    claims=int(claims)
    claim = Insurance_Claims.objects.filter(id=claims)
    claim.update(is_approved = True)
    claim=claim[0]
    request.session["claimID"] = claims
    (AMOUNT,reciever)=getar(claim)

    try:
      transaction = Transactions(ClaimID =claims, Sender=user,Reciever = reciever , Amount = AMOUNT)
      transaction.save()
      request.session["transaction"] = transaction.ID
      return redirect('payment')

    except:
      attributes = {"title":"Transaction",
                    "heading": "Something wrong with parameters",
                    "redirect":"login"}
      return render (request, "Common/Templates/message.html", attributes)


class Dashboard_Hospital (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
        request.session.get ("user_type", INVALID_USER_TYPE) != "Organization"):

      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    if(typeof.__eq__("Hospital")==False):
      return HttpResponseForbidden ()
    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Dashboard_Hospital.html", attributes)



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
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

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
      Patient.objects.filter (username=user.username).update (name=name, email=email,mobile_number=mobile_number,dob=dob)
      attributes = {"title":"Information update",
                    "heading": f"Information updated successfully for {name}",
                    "redirect":"/patient/dashboard"}
    except:
      attributes = {"title":"Information update",
                    "heading": f"Information could not be updated for {name}",
                    "redirect":"/patient/edit"}
    return render (request, "Common/Templates/message.html", attributes)


class Edit_Doctor (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Doctor"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Doctor")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Edit_Doctor.html", attributes)



  def post (self, request):
    if not (check_origin (request.META.get('HTTP_REFERER'))):
      return HttpResponseForbidden ()

    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Doctor"):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Doctor")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    location_address = request.POST['Location_address']
    location_district=request.POST['location_district']
    location_state=request.POST['location_state']
    location_country=request.POST['location_country']
    location_pin_code=request.POST['location_pin_code']
    try:
      Doctor.objects.filter (username=user.username).update(name=name, email=email,mobile_number=mobile_number,location_address=location_address,location_district=location_district,location_state=location_state,location_country=location_country,location_pin_code=location_pin_code)
      attributes = {"title":"Information update",
                    "heading": f"Information updated successfully for {name}",
                    "redirect":"/doctor/dashboard"}
    except:
      attributes = {"title":"Information update",
                    "heading": f"Information could not be updated for {name}",
                    "redirect":"/doctor/edit"}
    return render (request, "Common/Templates/message.html", attributes)




class Edit_Organization (ListView):
  def get (self, request):
    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Organization" ):
      return HttpResponseForbidden ()

    user = get_user (request.session.get ("username", INVALID_USERNAME), "Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")
    typeof=user.organization_type
    attributes = {"user":user}
    return render (request, "Dashboard/Templates/Edit_Organization.html", attributes)



  def post (self, request):
    if (request.session.get ("authenticated", False) == False or
      request.session.get ("user_type", INVALID_USER_TYPE) != "Organization" ):
      return HttpResponseForbidden ()
    user = get_user (request.session.get ("username", INVALID_USERNAME),"Organization")
    if (user == None):
      request.session["authenticated"] = False
      return redirect ("/login")

    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    description = request.POST['description']
    location_address = request.POST['Location_address']
    location_district=request.POST['location_district']
    location_state=request.POST['location_state']
    location_country=request.POST['location_country']
    location_pin_code=request.POST['location_pin_code']
    typeof=user.organization_type
    try:
      Organization.objects.filter (username=user.username).update(name=name, email=email,mobile_number=mobile_number,description=description,location_address=location_address,location_district=location_district,location_state=location_state,location_country=location_country,location_pin_code=location_pin_code)
      attributes = {"title":"Information update",
                    "heading": f"Information updated successfully for {name}",
                    "redirect":"/"+typeof+"/dashboard"}
    except:
      attributes = {"title":"Information update",
                    "heading": f"Information could not be updated for {name}",
                    "redirect":"/organization/edit"}
    return render (request, "Common/Templates/message.html", attributes)
