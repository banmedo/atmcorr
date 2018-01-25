
'''
Performs atmospheric correction and returns the corrected object
'''
def getCorrectedImage (credentials,args):
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

    return args
