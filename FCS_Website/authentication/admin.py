from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

class UserAdmin (admin.ModelAdmin):
  list_display = ("username", "name", "email","mobile_number")



class PatientAdmin (admin.ModelAdmin):
  list_display = ("username", "name", "email","mobile_number")



class DoctorAdmin (admin.ModelAdmin):
  list_display = ("username", "name", "email","mobile_number", "license_number")



class OrganizationImageInline (admin.TabularInline):
    model = OrganizationImage
    extra = 3



class OrganizationAdmin (admin.ModelAdmin):
  inlines = [OrganizationImageInline,]
  list_display = ("username", "name", "email","mobile_number", "location_state", "location_country", "location_pin_code")


class DocumentAdmin (admin.ModelAdmin):
  list_display = ("owner", "title","doc","is_verified")
admin.site.register (Patient, PatientAdmin)
admin.site.register (Doctor, DoctorAdmin)
admin.site.register (Organization, OrganizationAdmin)
# admin.site.register (document, DocumentAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)