"""Endpoints from PodPoint"""

AUTH = '/auth'
SESSIONS = '/sessions'
USERS = '/users'
PODS = '/pods'
UNITS = '/units'
CHARGE_SCHEDULES = '/charge-schedules'
CHARGES = '/charges'
CHARGE_OVERRIDE = '/charge-override'
FIRMWARE = '/firmware'

API_BASE = 'mobile-api.pod-point.com/api3/'
API_VERSION = 'v5'
API_BASE_URL = f"https://{API_BASE}{API_VERSION}"

"""Google endpoint, used for auth"""
GOOGLE_KEY = '?key=AIzaSyCwhF8IOl_7qHXML0pOd5HmziYP46IZAGU'
PASSWORD_VERIFY = f"/verifyPassword{GOOGLE_KEY}"
TOKEN = f"/token{GOOGLE_KEY}"

GOOGLE_BASE = 'www.googleapis.com/identitytoolkit/v3/relyingparty'
GOOGLE_BASE_URL = f"https://{GOOGLE_BASE}"

GOOGLE_TOKEN_BASE = 'securetoken.googleapis.com/v1'
GOOGLE_TOKEN_BASE_URL = f"https://{GOOGLE_TOKEN_BASE}"