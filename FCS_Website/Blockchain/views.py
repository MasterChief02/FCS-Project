from django.views.generic.list import ListView
from django.http import *

from .models import *

import time

# Create your views here.
class Show_Test (ListView):
  def get (self, request):
    Block_Chain.create_block (Document.objects.all ()[3], 0, "")
    return HttpResponseBadRequest ()