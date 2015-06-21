# -*- coding: utf-8 -*-

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

import configparser


def is_debug():
    return read_config('DEBUG', 'general') == 'True'


def read_config(name, section='general', default=None):
    if config.has_option(section, name):
        return config.get(section, name)
    return default


def read_config_section(section, default=None):
    if config.has_section(section):
        return config.items(section)
    return default


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def tmp_dir():
    return read_config('TMP_DIR', default='/tmp')


# Configurations from file
config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'settings.cfg')
priv_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                '.settings.cfg')

config = configparser.RawConfigParser()
config.read(config_file)
if os.path.isfile(priv_config_file):
    config.read(priv_config_file)

# Set APP_NAME
APP_NAME = read_config('APP_NAME', 'general', 'app')


#  Logging configuration
class TruncatePathFormatter(Formatter):
    def format(self, record):
        record.pathname = record.pathname.replace(
            "{0}/".format(os.path.dirname(__file__)), "")
        return super(TruncatePathFormatter, self).format(record)


logger_format = ("%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                 " | %(pathname)s:%(lineno)d")
#  Loggin to files is only allowed in debug mode on local dev box!
#  production logs are written to stdout, which uwsgi logs to files
#  stdout logging is also supported by popular cloud vendors
if is_debug():
    log_dir = read_config(
        'LOG_DIR', 'general',
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs'))

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_filename = os.path.join(log_dir, "server.log")

    vlh = RotatingFileHandler(log_filename, mode='a', maxBytes=50485760,
                              backupCount=5)
    vlh.setFormatter(TruncatePathFormatter(logger_format))

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(TruncatePathFormatter(logger_format))


def add_log_handlers(logger, force_info=False):
    if is_debug() and not force_info:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(vlh)
    else:
        logger.setLevel(logging.INFO)

    logger.addHandler(ch)


def getLogger(name=None):
    n = "{0}.{1}".format(APP_NAME, name) if name is not None else APP_NAME
    return logging.getLogger(n)


logger = getLogger()
add_log_handlers(logger)
logger = getLogger(__name__)



# Library log handling
library_log_handlers = read_config('LIBRARY_LOG_HANDLERS', 'general')
if library_log_handlers:
    for llh in library_log_handlers.split(','):
        add_log_handlers(logging.getLogger(llh))

logger.info("Initialized settings and setup logging")


def default_locale():
    return read_config('DEFAULT_LOCALE', 'general', 'no-NB')


def db_connection():
    res = "sqlite:///:memory:"
    if os.getenv('APP_CONTEXT_TEST') is None:
        host = read_config('HOST', 'postgresql')
        port = read_config('PORT', 'postgresql')
        name = read_config('DBNAME', 'postgresql')
        user = read_config('USER', 'postgresql')
        pwd = read_config('PASSWORD', 'postgresql')
        res = "postgresql://%s:%s@%s:%s/%s" % (user, pwd, host, port, name)
    else:
        logger.info("DB CONNECTION: %s" % res)
    return res
