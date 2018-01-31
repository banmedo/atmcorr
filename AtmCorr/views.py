from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import config
import ee

# Create your views here.
def index(request):
    #template = loader.get_template('AtmCorr/index.html'))
    context = {
        'key':'value'
    }
    return render(request, 'AtmCorr/index.html', context)

def getImageList(request):
    from .atmos.helpers.GetImages import getImageIds
    date = request.GET.get('date')
    north = request.GET.get('north')
    west = request.GET.get('west')
    south = request.GET.get('south')
    east = request.GET.get('east')
    maxZenith = request.GET.get('maxZenith')
    return JsonResponse(getImageIds(config.EE_CREDENTIALS, date, west, south, east, north, maxZenith))

def getMapId(request):
    from .atmos.helpers.GetImages import getMapId
    imgid = request.GET.get('id')
    return JsonResponse(getMapId(config.EE_CREDENTIALS,imgid))

def getCorrectedMapId(request):
    from .atmos.helpers.GetImages import getCorrectedMapId
    imgid = request.GET.get('id')
    return JsonResponse(getCorrectedMapId(config.EE_CREDENTIALS,imgid))

def exportImage(request):
    from .atmos.helpers.GetImages import exportImage
    imgid = request.GET.get('id')

    from oauth2client.service_account import ServiceAccountCredentials
    import googleapiclient.discovery
    import httplib2
    scope = 'https://www.googleapis.com/auth/drive'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.EE_PRIVATE_KEY_FILE, scope)
    http = credentials.authorize(httplib2.Http())
    serv = googleapiclient.discovery.build('drive', 'v2', http=http)

    return HttpResponse(exportImage(config.EE_CREDENTIALS,imgid))

def auth(request):
    from oauth2client.service_account import ServiceAccountCredentials
    import googleapiclient.discovery
    import httplib2
    scope = 'https://www.googleapis.com/auth/drive'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.EE_PRIVATE_KEY_FILE, scope)
    http = credentials.authorize(httplib2.Http())
    serv = googleapiclient.discovery.build('drive', 'v2', http=http)
    return HttpResponse("Done")
