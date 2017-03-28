from .models import Images
from .models import OrganizationInformation


def getBackgroundImage(request):

    photoList = Images.objects.all().filter(Page = Images.BACKGROUND)

    if len(photoList) >= 1:
        backgroundImage = photoList[0]
    	return {'backgroundImage': backgroundImage}
    else:
    	return {}

def getOrganizationInformation(request):

    organizationList = OrganizationInformation.objects.all()

    if len(organizationList) >= 1:
        organization = organizationList[0]
    	return {'organization': organization}
    else:
    	return {}