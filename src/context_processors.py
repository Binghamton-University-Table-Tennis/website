from .models import Location

def getPracticeLocation(request):

    locationList = Location.objects.all()

    if len(locationList) == 1:
        location = locationList[0]
    else:
        location = "TBD"

    return {'location': location}