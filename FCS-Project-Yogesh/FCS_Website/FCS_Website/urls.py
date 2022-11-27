"""FCS_Website URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from authentication.views import *
from Common.views import *
from Dashboard.views import *
from Documents.views import *
from OTP.views import *
from FCS_Website.settings import ROOT
# ROOT = '/FCS_Website/Data/Profile_Picture/'
# PATH = '/FCS_Website/Data/Profile_Picture/'

# ROOT = '/mnt/ntfs/IIITD/3rd Year/FCS/Project/FCS_Website/Documents/Data/Profile_Picture/'
PATH = '/images/'
urlpatterns = [

    # startup
    path('', Startup.as_view()),
    # Admin
    path ('admin/', admin.site.urls),

    # Authentication
    path ('login/', LoginPage.as_view ()),
    path ('logout/', LogoutPage.as_view ()),
    path ('signup/patient', Signup_Patient.as_view ()),
    path ('signup/doctor', Signup_Doctor.as_view ()),
    path ('signup/organization', Signup_Organization.as_view ()),

    # OTP
    path ('otp/', OTP.as_view ()),

    # Dashboard
    path ('patient/dashboard', Dashboard_Patient.as_view ()),
    path ('patient/dashboard', Dashboard_Patient.as_view ()),
    path ('doctor/dashboard', Dashboard_Doctor.as_view ()),
    path ('pharmacy/dashboard', Dashboard_Pharmacy.as_view ()),
    path ('insurance/dashboard', Dashboard_Insurance.as_view ()),
    path ('hospital/dashboard', Dashboard_Hospital.as_view ()),
    path ('patient/edit', Edit_Patient.as_view ()),
    path ('doctor/edit', Edit_Doctor.as_view ()),
    path ('organization/edit', Edit_Organization.as_view ()),

    # Document
    path ('document/add', Document_Add.as_view ()),
    path ('document/delete', Document_Delete.as_view ()),
    path ('document/share', Document_Share.as_view ()),
    path ('document/show', Document_Show.as_view ()),
    path ('document/docshare', Doctor_Share.as_view ()),

    # Common
    path ('list/doctors', Show_Doctors.as_view ()),
    path ('list/organization', Show_Organization.as_view ()),
    path ('list/patient', Show_Organization.as_view ()),



    # path('', HomePage.as_view(), name='home'),
    # path('', LoginPage.as_view(), name='login'),

    # path('logout/', LogoutPage.as_view(), name='logout'),
    # # path('register/', LoginPage.as_view(), name='register'),
    # path('PatientSignup/', PatientSignup.as_view(), name='PatientSignup'),
    # path('DoctorSignup/', DoctorSignup.as_view(), name='DoctorSignup'),
    # path('OrganizationSignup/', OrganizationSignup.as_view(), name='OrganizationSignup'),
    # path('Dashboard/',Dashboard.as_view(), name='Dashboard'),
    # path('OTP/',otp.as_view(), name='otp'),
    # path('document/add', document_add_view.as_view ()),
    # path('document/share', document_share_view.as_view ()),
    # path('document/show_shared', document_show_shared.as_view ()),
    # path('checkout/', home, name='home'),
    # path('create-checkout-session/', create_checkout_session, name='checkout'),
    # path('success.html/', success,name='success'),
    # path('cancel.html/', cancel,name='cancel'),
    # path('Signup/', Signup.as_view(), name='signup'),
]+ static(PATH, document_root=ROOT)
