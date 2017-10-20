import configparser

def configuration_get(section, key):
    Config = configparser.ConfigParser()
    Config.read("configuration/configuration.ini")
    try:
        configuration_value = Config.get(section, key)
        return configuration_value

    except(ValueError, NameError):
        print("Something went wrong with retrieving the value.")

def configuration_set(section, key, value):
    Config = configparser.ConfigParser()
    Config.read("configuration/configuration.ini")
    ConfigFile = open("configuration/configuration.ini", 'w')
    try:
        Config.set(section, key, value)

    except(configparser.NoSectionError, configparser.NoOptionError):
        print("This option or section does not exist.")

    Config.write(ConfigFile)
    ConfigFile.close()











# from cryptography.fernet import Fernet
#
# key = Fernet.generate_key()
# hive = Fernet(key)
#
#
# text = "Toine Lambalk how are you"
# message = text.encode('utf-8')
#
# encrypted = hive.encrypt(message)
#
# message = hive.decrypt(encrypted)
#
# test = message.decode('utf-8')
# print(test)
#
#
# print(key)