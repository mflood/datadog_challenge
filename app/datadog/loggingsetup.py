"""
    loggingsetup.py

    utility to set up logging
"""

import logging

LOGNAME = "datadog"

def init(loglevel=logging.DEBUG):
    """
        Creates standard logging
    """
    logger = logging.getLogger(LOGNAME)
    logger.setLevel(logging.DEBUG)
    channel = logging.StreamHandler()
    channel.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    channel.setFormatter(formatter)
    logger.addHandler(channel)
    logger.debug("Initialized logging")

    return logger
