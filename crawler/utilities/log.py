from os import path, makedirs
import logging

if not path.exists("logs/"):
    makedirs("logs/")
logging.basicConfig(
    filename="logs/HIVE.log",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG
)


def info(message):
    logging.info(msg=message)


def warning(message):
    logging.warning(msg=message)


def debug(message):
    logging.debug(msg=message)


def error(message):
    logging.error(msg=message)


def critical(message):
    logging.critical(msg=message)
