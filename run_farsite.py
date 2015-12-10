__author__ = 'Jesse Moy'

import re
import os
import time
import logging

import pywinauto
import pyautogui
from pywinauto.application import Application

from scripts.select_duration import *


# log_dir = 'E:/FIRE_MODELING/fire_model_python/log'
# logging.basicConfig(filename=(log_dir + '/fire_log.txt'),
#                     level=logging.DEBUG)

# Duration


def run_farsite(year):
    cond_month, cond_day, start_month, start_day, end_month, end_day = select_duration(year)
    ordinal_start = date(day=start_day, month=start_month, year=1409).toordinal()
    ordinal_end = date(day=end_day, month=end_month, year=1409).toordinal()

    logging.info('Start date: %r/%r/%r | End date:  %r/%r/%r | Duration: %r days'% (start_month,
                                                                                    start_day,
                                                                                    year,
                                                                                    end_month,
                                                                                    end_day,
                                                                                    year,
                                                                                    (ordinal_end-ordinal_start)))
    pyautogui.PAUSE = 0.25

    # full extent test input_dir
    input_dir = 'E:\\FIRE_MODELING\\fire_model_python\\bk_q_test\\inputs'

    farsite = pywinauto.application.Application()
    farsite.start_(r"C:\\Program Files (x86)\\farsite4.exe")

    # Load FARSITE project file
    logging.info('Loading FARSITE project file')

    # Open project window
    farsite_main_win = farsite.window_(title_re='.*FARSITE: Fire Area Simulator$')

    farsite_main_win.MenuItem('File->Load Project').Click()
    try:
        load_project = farsite.window_(title='Select Project File')
        load_project.SetFocus()

        pyautogui.typewrite(input_dir + '\\farsite\\manhattan.FPJ')
        pyautogui.press('enter')
        pyautogui.press('enter')

        logging.info('Project file loaded')

    except pywinauto.findwindows.WindowNotFoundError:
        logging.error('Can not find SELECT PROJECT FILE window')
        farsite.Kill_()

    # Load FARSITE landscape file
    logging.info('Loading FARSITE landscape file')

    # Open project input window
    farsite_main_win.MenuItem('Input-> Project Inputs').Click()

    try:
        project_inputs = farsite.window_(title='FARSITE Project')
        project_inputs.SetFocus()
        project_inputs[u'->13'].Click()

        # Load fuel and canopy rasters
        try:
            landscape_load = farsite.window_(title='Landscape (LCP) File Generation')
            landscape_load.SetFocus()
            pyautogui.press(['tab'] * 8)
            pyautogui.press('space')
            pyautogui.typewrite(input_dir + '\\farsite\\fuel.asc')
            pyautogui.press('enter')
            pyautogui.press(['down', 'space'])
            pyautogui.typewrite(input_dir + '\\farsite\\canopy.asc')
            pyautogui.press('enter')
            pyautogui.press('enter')

        except pywinauto.findwindows.WindowNotFoundError:
            logging.error('Can not find Landscape (LCP) File Generation window')
            farsite.Kill_()

        # Wait while FARSITE generates the landcape file
        landscape_generated = farsite.window_(title_re='.*Landscape Generated$')
        landscape_generated.Wait('exists', timeout=60)
        landscape_generated.SetFocus()
        pyautogui.press('enter')
        pyautogui.press('esc')

        logging.info('landscape file loaded')

    except pywinauto.findwindows.WindowNotFoundError:
        logging.info('Unable to generate landscape file')
        farsite.Kill_()

    # Delete FARSITE_output from output folder
    logging.info('Deleting previous FARSITE outputs')
    for f in os.listdir((input_dir + '\\script\\burn_rasters')):
        if re.search('farsite_output', f):
            os.remove(((input_dir + '\\script\\burn_rasters') + '\\' + f))

    # Export and output options
    logging.info('Setting export and output options')

    # Open export and output option window
    farsite_main_win.MenuItem('Output->Export and Output').Click()
    try:
        set_outputs = farsite.window_(title='Export and Output Options')
        set_outputs.SetFocus()
        set_outputs[u'&Select Rater File Name'].Click()
        pyautogui.typewrite(input_dir + '\\script\\burn_rasters\\farsite_output')
        pyautogui.press('enter')
        set_outputs[u'Flame Length (m)'].Click()
        set_outputs[u'&Default'].Click()
        set_outputs[u'&OK'].Click()
        logging.info('Outputs set')

    except pywinauto.findwindows.WindowNotFoundError:
        logging.error('Can not find EXPORT AND OUTPUT OPTIONS window')
        farsite.Kill_()

    # Set simulation parameters
    logging.info('Setting simulation parameters')

    # Open parameter window
    farsite_main_win.MenuItem('Model->Parameters').Click()
    try:
        set_parameters = farsite.window_(title='Model Parameters')
        set_parameters.SetFocus()
        pyautogui.press(['right'] * 90)
        pyautogui.press(['tab'] * 2)
        pyautogui.press(['left'] * 30)
        pyautogui.press('tab')
        pyautogui.press(['left'] * 20)
        pyautogui.press('enter')
        time.sleep(3)
        logging.info('Parameters set')

    except pywinauto.findwindows.WindowNotFoundError:
        logging.error('Can not find MODEL PARAMETERS window')
        farsite.Kill_()

    # fire behavior options: disable crown fire
    # Open fire behavior window
    farsite_main_win.MenuItem('Model->Fire Behavior Options').Click()
    try:
        set_fire_behavior = farsite.window_(title='Fire Behavior Options')
        set_fire_behavior.SetFocus()
        set_fire_behavior[u'Enable Crownfire'].UnCheck()
        set_fire_behavior[u'&OK'].Click()
        # pyautogui.press(['space', 'enter'])

    except pywinauto.findwindows.WindowNotFoundError:
        logging.error('can not find FIRE BEHAVIOR OPTIONS window')
        farsite.Kill_()

    # Set number of simulation threads
    farsite_main_win.MenuItem('Simulate->Options').Click()
    try:
        simulation_options = farsite.window_(title='Simulation Options')
        simulation_options.SetFocus()
        simulation_options.Wait('ready')
        simulation_options.UpDown.SetValue(8)
        simulation_options[u'&OK'].Click()

    except pywinauto.findwindows.WindowNotFoundError:
        logging.error('can not find SIMULATION OPTIONS window')
        farsite.Kill_()

    # Open duration window
    farsite_main_win.MenuItem('Simulate->Duration').Click()
    try:
        simulation_duration = farsite.window_(title='Simulation Duration')
        simulation_duration.SetFocus()
        simulation_duration[u'Use Conditioning Period for Fuel Moistures'].Click()
        time.sleep(.5)
        # Conditioning month
        while int(simulation_duration[u'Static5'].Texts()[0]) != cond_month:
            if int(simulation_duration[u'Static5'].Texts()[0]) > cond_month:
                simulation_duration.Updown1.Decrement()
            if int(simulation_duration[u'Static5'].Texts()[0]) < cond_month:
                simulation_duration.Updown1.Increment()

        # Conditioning day
        while int(simulation_duration[u'Static6'].Texts()[0]) != cond_day:
            if int(simulation_duration[u'Static6'].Texts()[0]) > cond_day:
                simulation_duration.Updown2.Decrement()
            if int(simulation_duration[u'Static6'].Texts()[0]) < cond_day:
                    simulation_duration.Updown2.Increment()

        # Start month
        while int(simulation_duration[u'Static9'].Texts()[0]) != start_month:
            if int(simulation_duration[u'Static9'].Texts()[0]) > start_month:
                simulation_duration.Updown5.Decrement()
            if int(simulation_duration[u'Static9'].Texts()[0]) < start_month:
                simulation_duration.Updown5.Increment()

        # Start day
        while int(simulation_duration[u'Static10'].Texts()[0]) != start_day:
            if int(simulation_duration[u'Static10'].Texts()[0]) > start_day:
                simulation_duration.Updown6.Decrement()
            if int(simulation_duration[u'Static10'].Texts()[0]) < start_day:
                simulation_duration.Updown6.Increment()

        # End month
        while int(simulation_duration[u'Static13'].Texts()[0]) != end_month:
            if int(simulation_duration[u'Static13'].Texts()[0]) > end_month:
                simulation_duration.Updown9.Decrement()
            if int(simulation_duration[u'Static13'].Texts()[0]) < end_month:
                simulation_duration.Updown9.Increment()
        # End day
        while int(simulation_duration[u'Static14'].Texts()[0]) != end_day:
            if int(simulation_duration[u'Static14'].Texts()[0]) > end_day:
                simulation_duration.Updown10.Decrement()
            if int(simulation_duration[u'Static14'].Texts()[0]) < end_day:
                simulation_duration.Updown10.Increment()

        simulation_duration[u'OK'].Click()

        logging.info('Duration set')

    except farsite.findwindows.WindowNotFoundError:
        logging.info('can not find SIMULATION DURATION window')
        farsite.Kill_()

    # Initiate simulation
    farsite_main_win.MenuItem('Simulate->Initiate/Terminate').Click()
    landscape_initiated = farsite.window_(title_re='.*LANDSCAPE:')
    landscape_initiated.Wait('ready', timeout=40)

    time.sleep(5)

    # Set Ignition
    farsite_main_win.MenuItem('Simulate->Modify Map->Import Ignition File').Click()
    try:
        set_ignition = farsite.window_(title='Select Vector Ignition File')
        set_ignition.SetFocus()
        pyautogui.press('right')
        pyautogui.typewrite(input_dir + '\\farsite\\ignition.vct')
        pyautogui.press('enter')
        pyautogui.press(['right', 'enter'])
        pyautogui.press(['right', 'enter'])

    except farsite.findwindows.WindowNotFoundError:
            logging.error('can not find SELECT VECTOR IGNITION FILE window')

    logging.info('Starting simulation')
    farsite_main_win.SetFocus()
    farsite_main_win.MenuItem(u'&Simulate->&Start/Restart').Click()
    simulation_complete = farsite.window_(title_re='.*Simulation Complete')
    simulation_complete.Wait('exists', timeout=1800)
    simulation_complete.SetFocus()
    pyautogui.press('enter')

    # Exit FARSITE
    farsite.Kill_()
    pyautogui.press('enter')

# run_farsite()
