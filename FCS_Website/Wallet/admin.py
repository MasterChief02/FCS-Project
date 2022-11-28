from django.contrib import admin
from Wallet.models import Insurance_Claims,Transactions
# Register your models here.
class ClaimAdmin (admin.ModelAdmin):
  list_display = ("firm", "amount","patient","is_approved")
class TAdmin (admin.ModelAdmin):
  list_display = ("ID", "Sender","Reciever","Amount")
admin.site.register (Insurance_Claims,ClaimAdmin) 
admin.site.register (Transactions,TAdmin) 