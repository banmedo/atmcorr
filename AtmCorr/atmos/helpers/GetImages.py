'''
Returns the dates of all available images within specified range
'''
import json

def getImageDates(credentials, filters):
    import ee
    ee.Initialize(credentials)

    geom = ee.Geometry.Point(filters['geom'][0], filters['geom'][1])

    ic = ee.ImageCollection(filters['mission'])\
        .filterBounds(geom)\
        .filterDate(filters['start'],filters['end'])\
        .filter(ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',filters['MEAN_SOLAR_ZENITH_ANGLE']))

    imageDates = []


    return "asd"

def getImageIds(credentials, date, west, south, east, north, maxZenith):
    import ee
    ee.Initialize(credentials)
    geom = ee.Geometry.Rectangle(float(west), float(south), float(east), float(north))
    start = ee.Date(date)
    end = start.advance(1,'day')
    ic = ee.ImageCollection('COPERNICUS/S2')\
        .filterDate(start,end)\
        .filterBounds(geom)\
        .filter(ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',int(maxZenith)))

    def iter(image, passlist):
        return ee.List(passlist).add(image.id())

    idList = ee.List(ic.iterate(iter,ee.List([])))

    return {'idlist':idList.getInfo()}
