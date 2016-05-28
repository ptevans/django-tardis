from datetime import datetime, timedelta

from django.http import HttpResponse
from tardis.models import Trip


def what_time_is_it(request, *args, **kawrgs):
    response = HttpResponse(str(datetime.now()))
    t = Trip(destination_date=datetime.now() + timedelta(days=2),
             step_size=60)
    t.save()
    t.start()
    return response
