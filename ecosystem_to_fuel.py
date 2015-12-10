__author__ = 'Jesse Moy'

import numpy


# Creates a fuel array based on ecosystem type and time since last disturbance
def ecosystem_to_fuel(ecosystem_array,
                      last_disturbance_array,
                      fuel_array,
                      translation):

    # Constants
    succession_time_mid = 10
    succession_time_climax = 20

    for index, cell_value in numpy.ndenumerate(ecosystem_array):
            row_index = index[0]
            col_index = index[1]

            if last_disturbance_array[row_index][col_index] > succession_time_climax:
                fuel_array[row_index][col_index] = translation[cell_value]['climax_fuel']

            elif last_disturbance_array[row_index][col_index] > succession_time_mid:
                fuel_array[row_index][col_index] = translation[cell_value]['mid_fuel']

            else:
                fuel_array[row_index][col_index] = translation[cell_value]['new_fuel']

    return fuel_array
