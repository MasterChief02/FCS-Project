from authentication.models import *



INVALID_USERNAME = "ABBA_JABBA_DABBA"
INVALID_USER_TYPE = "TYPE"

HOST_ORIGIN = "localhost:8000"


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


def check_origin (origin):
  if (str (origin).split ("/")[2] == HOST_ORIGIN):
    return True
  return False