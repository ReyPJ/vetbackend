from django.http import HttpResponse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def set_admin_cookie(request):
    response = HttpResponse("Cookie de admin set")
    utc_now = datetime.now(ZoneInfo("UTC"))
    expires = utc_now + timedelta(days=1)
    response.set_cookie('isAdmin', 'true', expires=expires, httponly=True, secure=True)
    return response