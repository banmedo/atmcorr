'''
Returns the dates of all available images within specified range
'''
import json


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

    se = SixS_emulator(mission)

    iLUTs = Interpolated_LUTs(mission)

    iLUTs.interpolate_LUTs()
    se.iLUTs = iLUTs.get()

    return 1
