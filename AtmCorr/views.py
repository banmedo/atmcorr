from django.shortcuts import render
from django.http import HttpResponse
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
    from .atmos.helpers import GetCorrectedImage
    return HttpResponse("defined")
