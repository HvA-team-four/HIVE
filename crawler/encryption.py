from cryptography.fernet import Fernet
import configuration


def what_is_the_encryption_key():
    if (configuration.configuration_get("database", "key") == "not set"):
        encryption_key = Fernet.generate_key()
        encryption_key = encryption_key.decode('utf-8')
        configuration.configuration_set("database", "key", encryption_key)
        print("Encryption key generated.")

    key = configuration.configuration_get("database", "key").encode('utf-8')
    hive = Fernet(key)
    return hive

def hive_encrypt(message):
    encryption_key = what_is_the_encryption_key()

    unencrypted_message = message.encode('utf-8')
    encrypted_message = encryption_key.encrypt(unencrypted_message)
    undecoded_message = encrypted_message.decode('utf-8')

    return undecoded_message

def hive_decrypt(message):
    encryption_key = what_is_the_encryption_key()

    undecoded_message = message.encode('utf-8')
    encrypted_message = encryption_key.decrypt(undecoded_message)
    decrypted_message = encrypted_message.decode('utf-8')

    return decrypted_message