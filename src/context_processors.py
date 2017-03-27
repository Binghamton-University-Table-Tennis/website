from .models import Location
from .models import Images


def getPracticeLocation(request):

    locationList = Location.objects.all()

    if len(locationList) == 1:
        location = locationList[0].Description
    else:
        location = "TBD"

    return {'location': location}