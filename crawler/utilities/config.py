from configparser import ConfigParser, NoOptionError, NoSectionError
import log
from os import path

CONFIGURATION_FILE_PATH = path.abspath(path.join(path.abspath(__file__), "..", "..", "..", "configuration.ini"))
config = ConfigParser()
config.read(CONFIGURATION_FILE_PATH)

def location_configuration():
    return(CONFIGURATION_FILE_PATH)

def check_configuration():
    CONFIGURATION_FILE_PATH = path.abspath(path.join(path.abspath(__file__), "..", "..", "..", "configuration.ini"))

    config = ConfigParser()
    return(config.read(CONFIGURATION_FILE_PATH))

def configuration_get(section, key):
    try:
        return config.get(section, key)
    except(ValueError, NameError) as e:
        log.error(str(e))


def configuration_set(section, key, value):
    config_file = open(CONFIGURATION_FILE_PATH, 'w')
    try:
        config.set(section, key, value)

    except(NoSectionError, NoOptionError) as e:
        log.error(str(e))

    config.write(config_file)
    config_file.close()