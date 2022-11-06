from authentication.models import *


def get_user (username:str, type:str):
  if (type.__eq__("Patient")):
    user = Patient
  elif (type.__eq__("Doctor")):
    user = Doctor
  elif (type.__eq__("Organization")):
    user = Organization
  else:
    return None

  users = user.objects.filter (username=username)
  if len (users) > 0:
    return users[0]
  return None
