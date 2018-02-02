'''
Returns the dates of all available images within specified range
'''
import json
import time
import random
import string

__MISSION__ = 'COPERNICUS/S2'

def getImageIds(credentials, date, west, south, east, north, maxZenith):
    import ee
    ee.Initialize(credentials)
    geom = ee.Geometry.Rectangle(float(west), float(south), float(east), float(north))
    start = ee.Date(date)
    end = start.advance(1,'day')
    ic = ee.ImageCollection(__MISSION__)\
        .filterDate(start,end)\
        .filterBounds(geom)\
        .filter(ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',int(maxZenith)))

    def iter(image, passlist):
        return ee.List(passlist).add(image.id())

    idList = ee.List(ic.iterate(iter,ee.List([])))

    return {'idlist':idList.getInfo()}

def getMapId(credentials, id):
    import ee
    ee.Initialize(credentials)
    img = ee.Image(__MISSION__+'/'+id)
    img = img.divide(10000)
    mapId = img.getMapId({'bands':'B4,B3,B2','min':0,'max':0.25,'gamma':1.5});
    temp = {
        'mapid': mapId['mapid'],
        'token': mapId['token']
    }
    return temp

def getCorrectedImage(credentials, id):
    import ee
    ee.Initialize(credentials)
    img = ee.Image(__MISSION__+'/'+id)

    import os
    import sys

    sys.path.append(os.path.join(os.getcwd(),'AtmCorr','atmos','bin'))

    from sixs_emulator_ee_sentinel2_batch import SixS_emulator
    from atmcorr_input import Atmcorr_input
    from atmospheric_correction import atmospheric_correction
    from radiance import radiance_from_TOA
    from interpolated_LUTs import Interpolated_LUTs

    se = SixS_emulator(__MISSION__)

    iLUTs = Interpolated_LUTs(__MISSION__)

    iLUTs.interpolate_LUTs()
    se.iLUTs = iLUTs.get()

    Atmcorr_input.geom = img.geometry().centroid()
    feature = Atmcorr_input.extractor(img).getInfo()

    atSensorRad = radiance_from_TOA(img, feature)
    seResult = se.run(feature['properties']['atmcorr_inputs'])
    corrected = ee.Image(atmospheric_correction(atSensorRad, seResult))

    return corrected

def getCorrectedMapId(credentials, id):
    import ee
    ee.Initialize(credentials)

    corrected = getCorrectedImage(credentials, id)
    correctMapId = corrected.getMapId({'bands':'B4,B3,B2','min':0,'max':0.25,'gamma':1.5});

    tempCorrected = {
        'mapid': correctMapId['mapid'],
        'token': correctMapId['token']
    }
    return tempCorrected

def exportImage(credentials, id):
    import ee
    ee.Initialize(credentials)

    image = ee.Image(ee.ImageCollection('COPERNICUS/S2').first())
    image = image.uint32()

    rnd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    date = str(int(time.time()))
    filePrefix = date+rnd

    task = ee.batch.Export.image(
        image=image,
        description="exported_image",
        #region=image.geometry().bounds().getInfo()['coordinates'],
        config={
            'driveFileNamePrefix': filePrefix
        })

    task.start()
    return  {"taskid":task.id,"fileprefix":filePrefix}
