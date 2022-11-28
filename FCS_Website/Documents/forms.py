from django import forms

# class Document_Add_Form (forms.forms):
#     pass

class Document_Share_Others_Form (forms.Form):
  username = forms.CharField ()
  name = forms.CharField ()
  private_key = forms.CharField ()
  file = forms.FileField ()

class Document_Add_Patient_form (forms.Form):
  name = forms.CharField ()
  file = forms.FileField ()