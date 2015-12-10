__author__ = 'Jesse Moy'


def ecosystem_to_fuel(ecosystem_array,
                      last_disturbance_array,
                      fuel_array,
                      translation):

    # Constants
    succession_time_mid = 10
    succession_time_climax = 20

    for row_index, row_value in enumerate(ecosystem_array):
        for col_index, cell_value in enumerate(row_value):

            if last_disturbance_array[row_index][col_index] > succession_time_climax:
                fuel_array[row_index][col_index] = translation[cell_value]['climax_fuel']

            elif last_disturbance_array[row_index][col_index] > succession_time_mid:
                fuel_array[row_index][col_index] = translation[cell_value]['mid_fuel']

            else:
                fuel_array[row_index][col_index] = translation[cell_value]['new_fuel']

    return fuel_array
