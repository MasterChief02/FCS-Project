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
from Documents.views import *

from authentication.views import *


urlpatterns = [
    path ('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    # path('register/', LoginPage.as_view(), name='register'),
    path('PatientSignup/', PatientSignup.as_view(), name='PatientSignup'),
    path('DoctorSignup/', DoctorSignup.as_view(), name='DoctorSignup'),
    path('PharmacySignup/', PharmacySignup.as_view(), name='PatientSignup'),
    path('HospitalSignup/', HospitalSignup.as_view(), name='DoctorSignup'),
    path('InsuranceFirmSignup/', InsuranceFirmSignup.as_view(), name='PatientSignup'),
    path('Payment/',PaymentPage.as_view(), name='Payment'),
    path('Dashboard/',Dashboard.as_view(), name='Dashboard'),
    path('OTP/',otp.as_view(), name='otp'),
    path('document/add', document_add_view.as_view ()),
    path('document/share', document_share_view.as_view ())
    path('document/show_shared', document_show_shared.as_view ())
]
