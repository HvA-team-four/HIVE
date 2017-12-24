#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser, NoOptionError, NoSectionError
from os import path

from log import *

# Setting variables
CONFIGURATION_FILE_PATH = path.abspath(path.join(path.abspath(__file__), "..", "..", "..", "configuration.ini"))
config = ConfigParser()
config.read(CONFIGURATION_FILE_PATH)


def location_configuration():
    """This function returns the location of the configuration file on the machine. This function is called from the
    configuration-settings page.
    """
    return(CONFIGURATION_FILE_PATH)


def check_configuration():
    """This function checks whether the configuration file exists at the configuration file location. This function
    returns a boolean value.
    """
    CONFIGURATION_FILE_PATH = path.abspath(path.join(path.abspath(__file__), "..", "..", "..", "configuration.ini"))

    config = ConfigParser()
    return(config.read(CONFIGURATION_FILE_PATH))


def configuration_get(section, key):
    """This function is used to get the value of a key in a certain section. The section is the file is the value
    between the brackets [] and the key is the value after the colon.
    """
    try:
        return config.get(section, key)
    except(ValueError, NameError) as e:
        log.error(str(e))


def configuration_set(section, key, value):
    """This function is used to set the value of a key in a certain section.
    """
    config_file = open(CONFIGURATION_FILE_PATH, 'w')
    try:
        config.set(section, key, value)

    except(NoSectionError, NoOptionError) as e:
        log.error(str(e))

    config.write(config_file)
    config_file.close()