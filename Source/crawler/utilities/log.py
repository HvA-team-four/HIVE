#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In order to use the logging functionality you need to import the following if its not already imported:
from utilities import log

In order to write to log use the following format:
log.<loglevel>('Message to write in logfile')
The <loglevel> should be one of following levels: info, warning, debug, error, critical.

depending on the level of logging that we have set certain messages will or will not appear in the file. For instance,
if we change the logging level to "error" only messages of level error and above will be added to the logfile. For now
the "debug" level shows all messages in the logfile.
"""

from os import path, makedirs
import logging

pathname = path.dirname(path.realpath(__file__))

if not path.exists("{}/logs/".format(pathname)):
    makedirs("{}/logs/".format(pathname))

logging.basicConfig(
    filename="{}/logs/hive.log".format(pathname),
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
