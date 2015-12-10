__author__ = 'Jesse Moy'

import numpy

# Convert numpy to ASCII raster for use in FARSITE
def array_to_raster(out_path, array, header):

    out_asc = open(out_path, 'w')
    for attribute in header:
        out_asc.write(attribute)

    numpy.savetxt(out_asc, array, fmt="%4i")
    out_asc.close()