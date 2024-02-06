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
API_BASE_URL = 'https://' + API_BASE + '/' + API_VERSION

"""Google endpoint, used for auth"""
GOOGLE_KEY = '?key=AIzaSyCwhF8IOl_7qHXML0pOd5HmziYP46IZAGU'
PASSWORD_VERIFY = '/verifyPassword' + GOOGLE_KEY

GOOGLE_BASE = 'www.googleapis.com/identitytoolkit/v3/relyingparty'
GOOGLE_BASE_URL = 'https://' + GOOGLE_BASE
