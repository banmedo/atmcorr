from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from . import config
import ee

def getUserAuth():
    userAuth = GoogleAuth(settings_file='settings.yaml')
    userAuth.LoadCredentialsFile('credentials.txt')
    if userAuth.credentials is None:
        #userAuth.LocalWebserverAuth()
        return {'loggedin':False,'auth':userAuth}
    elif userAuth.access_token_expired:
        userAuth.Refresh()
    else:
        userAuth.Authorize()
    return {'loggedin':True,'auth':userAuth}

# Create your views here.
def index(request):
    #template = loader.get_template('AtmCorr/index.html'))
    context = {
        'key':'value'
    }
    logState = getUserAuth()
    if not logState['loggedin']:
        userAuth = logState['auth']
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
    from .atmos.helpers.GetImages import exportImage, resumeWhenTaskComplete
    #get image id from request
    imgid = request.GET.get('id')
    #get user authentication
    logState = getUserAuth()
    #retun auth url to be handled in js if user has not authenticated app
    if not logState['loggedin']:
        userAuth = logState['auth']
        return JsonResponse({'success':False,'authurl':userAuth.GetAuthUrl()})
    #perform export task if user authenticated
    else:
        #export correct image to service account drive and get taskid
        task = exportImage(config.EE_CREDENTIALS,imgid)
        taskid = task['taskid']
        prefix = task['fileprefix']
        #wait till task comp;ete
        taskDone =resumeWhenTaskComplete(taskid)
        #authenticate pydrive with user and service drives
        userAuth = logState['auth']
        userDrive = GoogleDrive(userAuth)

        serviceAuth = GoogleAuth()
        scope = ['https://www.googleapis.com/auth/drive']
        serviceAuth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.EE_PRIVATE_KEY_FILE,
        scope)
        serviceDrive = GoogleDrive(serviceAuth)

        #find file in service account drive
        prefix_with_escaped_quotes = prefix.replace('"', '\\"')
        query = 'title contains "%s"' % prefix_with_escaped_quotes
        fileList = serviceDrive.ListFile({'q':query}).GetList()
        reqFile = fileList[0]
        #make the file public
        newPermit = reqFile.InsertPermission({
        'type':'anyone',
        'value':'anyone',
        'role':'reader'})
        #get file id to copy
        fid = reqFile.get('id')
        #copy the file to user's google drive
        newFile = userDrive.auth.service.files().copy(fileId=fid,body={'title':prefix}).execute()
        #return success state and file download url
        return JsonResponse({'success':True,'fileURL':newFile['alternateLink']})

def oauth2callback(request):
    code = request.GET.get('code')
    userAuth = GoogleAuth()
    userAuth.Auth(code)
    userAuth.SaveCredentialsFile('credentials.txt')
    return HttpResponseRedirect('/AtmCorr')
