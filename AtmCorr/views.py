from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from . import config
import ee

def getUserAuth():
    userAuth = GoogleAuth(settings_file='settings.yaml')
    userAuth.LoadCredentialsFile("credentials.txt")
    if userAuth.credentials is None:
        #userAuth.LocalWebserverAuth()
        return {"loggedin":False,"auth":userAuth}
    elif userAuth.access_token_expired:
        userAuth.Refresh()
    else:
        userAuth.Authorize()
    return {"loggedin":True,"auth":userAuth}

# Create your views here.
def index(request):
    #template = loader.get_template('AtmCorr/index.html'))
    context = {
        'key':'value'
    }
    logState = getUserAuth()
    if not logState["loggedin"]:
        userAuth = logState["auth"]
        return HttpResponseRedirect(userAuth.GetAuthUrl())
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
    return JsonResponse(exportImage(config.EE_CREDENTIALS,imgid))

def auth(request):

    userDrive = GoogleDrive(userAuth)

    serviceAuth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    serviceAuth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.EE_PRIVATE_KEY_FILE,
        scope)
    serviceDrive = GoogleDrive(serviceAuth)

    prefix = "1517464801UNOPJ"
    #prefix = "exported_image"
    prefix_with_escaped_quotes = prefix.replace('"', '\\"')
    query = 'title contains "%s"' % prefix_with_escaped_quotes
    fileList = serviceDrive.ListFile({'q':query}).GetList()
    reqFile = fileList[0]
    newPermit = reqFile.InsertPermission({
        'type':'anyone',
        'value':'anyone',
        'role':'reader'})

    fid = reqFile.get('id')

    #newFile = userDrive.auth.service.files().copy(fileId=fid,body={'title':prefix}).execute()

    return HttpResponse(fid)#newFile['alternateLink'])

def oauth2callback(request):
    code = request.GET.get('code')
    userAuth = GoogleAuth()
    userAuth.Auth(code)
    userAuth.SaveCredentialsFile("credentials.txt")
    return HttpResponseRedirect("/AtmCorr")
