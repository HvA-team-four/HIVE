from configparser import ConfigParser, NoOptionError, NoSectionError
from .log import error
from os import path

CONFIGURATION_FILE_PATH = path.join("..", "..", "configuration.ini")

config = ConfigParser()
config.read(CONFIGURATION_FILE_PATH)


def configuration_get(section, key):
    try:
        return config.get(section, key)
    except(ValueError, NameError) as e:
        print(error(str(e)))


def configuration_set(section, key, value):
    config_file = open(CONFIGURATION_FILE_PATH, 'w')
    try:
        config.set(section, key, value)

    except(NoSectionError, NoOptionError) as e:
        error(str(e))

    config.write(config_file)
    config_file.close()
