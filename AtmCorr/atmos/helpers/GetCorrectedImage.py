
'''
Performs atmospheric correction and returns the corrected object
'''
def getCorrectedImage (credentials,mapID):
    import ee
    ee.Initialize(credentials)

    import os
    import sys

    sys.path.append(os.path.join(os.getcwd(),'AtmCorr','atmos','bin'))

    from sixs_emulator_ee_sentinel2_batch import SixS_emulator
    from atmcorr_input import Atmcorr_input
    from atmospheric_correction import atmospheric_correction
    from radiance import radiance_from_TOA
    from interpolated_LUTs import Interpolated_LUTs

    # a place and a mission
    geom = ee.Geometry.Point(77.8574, 30.2211)
    mission = 'COPERNICUS/S2'

    se = SixS_emulator(mission)

    ic = ee.ImageCollection(mission)\
        .filterBounds(geom)\
        .filterDate('2016-06-01','2016-06-30')\
        .filter(ee.Filter.lt('MEAN_SOLAR_ZENITH_ANGLE',75))

    iLUTs = Interpolated_LUTs(mission)

    iLUTs.interpolate_LUTs()
    se.iLUTs = iLUTs.get()

    # extract atmcorr inputs as feature collection
    Atmcorr_input.geom = geom  # specify target location (would use image centroid otherwise)
    atmcorr_inputs = ic.map(Atmcorr_input.extractor).getInfo()
    features = atmcorr_inputs['features']

    # atmospherically correct image collection

    ic_atmospherically_corrected = []
    '''
    for feature in features:

        # at-sensor radiance
        toa = ee.Image(mission+'/'+feature['properties']['imgID'])
        rad = radiance_from_TOA(toa, feature)

        # 6S emulator
        cc = se.run(feature['properties']['atmcorr_inputs'])

        # atmospheric correction
        SR = atmospheric_correction(rad, cc)

        toa_id = toa.getMapId();
        ic_atmospherically_corrected.append(SR)

    # Earth Engine image collection
    ic_atmospherically_corrected = ee.ImageCollection(ic_atmospherically_corrected)

    SR = ee.Image(ic_atmospherically_corrected.first())
    afterMapId = SR.getMapId()
    temp = {
        "mapId" : afterMapId['mapid'],
        "token" : afterMapId['token']
    }'''
    temp = {"Asdasd":"qweqwe"}
    return temp
