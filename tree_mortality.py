__author__ = 'LabGuest'

import math
import random


# Tree_mortality calculates the percentage of the canopy in a cell killed during a burning event
# This estimate is based on the age of the forest and the length of the flame
# Model logic and tree size/diameter regressions from Tim Bean
def tree_mortality(flame, age):

    # Convert flame length to ft
    flame *= 3.2808399

    # Calculate scorch height
    scorch = (3.1817*(flame**1.4503))

    # Calculate tree height
    tree_height = 44 * math.log(age) - 93

    # Calculate tree diameter at breast height
    DBH = (25.706 * math.log(age))-85.383

    if tree_height < 0:
        tree_height = 1
    if age <= 35:
        DBH = 5
    if age <= 25:
        DBH = 3
    if age <= 20:
        DBH = 2
    if age <= 15:
        DBH = 1

    # Calculate bark thickness
    bark_thickness = 0.045 * DBH

    # Define crown ratio
    crown_ratio = 0.4

    # Calculate crown height
    crown_height = tree_height*(1-crown_ratio) #calc crown height

    # Calculate crown kill
    if scorch < crown_height:
        crown_kill = 0


    else:

        crown_kill = 41.961 * (math.log (100*(scorch - crown_height)/(tree_height * crown_ratio)))-89.721

        if crown_kill < 5:
            crown_kill = 5

        if crown_kill > 100:
            crown_kill = 100

    # Calculate percent mortality
    mortality = (1/(1 + math.exp((-1.941+(6.3136*(1-(math.exp(-bark_thickness)))))-(.000535*(crown_kill**2)))))

    return mortality
    #print 'Age: %r\t| Height: %r\t| DBH %r\t | Crown Kill: %r\t| Mortality: %r' %(age, tree_height, DBH, ck, pm)