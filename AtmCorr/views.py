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

def getSrtmMap(request):
    """Request an image from Earth Engine and render it to a web page."""
    ee.Initialize(config.EE_CREDENTIALS)
    mapid = ee.Image('srtm90_v4').getMapId({'min': 0, 'max': 1000})

    # These could be put directly into template.render, but it
    # helps make the script more readable to pull them out here, especially
    # if this is expanded to include more variables.
    return HttpResponse(mapid.__str__())

def getSomething(request):
    from .atmos.helpers.GetCorrectedImage import getCorrectedImage
    trestResponse = {"Asdasd":"asdasd"}
    return JsonResponse(getCorrectedImage(config.EE_CREDENTIALS,trestResponse))

def getImageList(request):
    from .atmos.helpers.GetImages import getImageCount
    date = request.GET.get('date')
    north = request.GET.get('north')
    west = request.GET.get('west')
    south = request.GET.get('south')
    east = request.GET.get('east')

    '''
    mission = 'COPERNICUS/S2'
    filters = {
        'mission' : mission,
        'geom' : [77.8574, 30.2211],
        'start' : '2016-06-01',
        'end' : '2016-06-30',
        'MEAN_SOLAR_ZENITH_ANGLE' : 75
    }
    return HttpResponse(getImageDates(config.EE_CREDENTIALS, filters))'''
    return HttpResponse(getImageCount(config.EE_CREDENTIALS, date, west, south, east, north))
