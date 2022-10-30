from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

class UserAdmin (admin.ModelAdmin):
  list_display = ("username", "email",)



class PatientAdmin (admin.ModelAdmin):
  list_display = ("username", "email", "aadhar", "mobile_number", "dob")



class OrganizationAdmin (admin.ModelAdmin):
  list_display = ("username", "email", "name", "description", "image_1", "image_2", "image_3", "image_4", "image_5")




admin.site.register (patient, PatientAdmin)
admin.site.register (organization, OrganizationAdmin)
admin.site.register (user, UserAdmin)
admin.site.register (insurance_firm,OrganizationAdmin)
admin.site.register (doctor,OrganizationAdmin)
admin.site.register (hospital,OrganizationAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)