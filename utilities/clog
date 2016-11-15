# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                clog.py
Class wrapper to minimize code duplication when using logging inside a project.
The class receives two parameters. 
A ConfigParser instance with necessary data and a list of log names, with their level inside each name.
Additionaly, an optional parameter can be passed to change the log path. The default behaviour is to use the path conf especifies.

Example:
from utilities import clog
ilog = clog.Clog(conf, [main_log_DEBUG.log, main_log_INFO.log, main_log_ERROR.log])

***********************************************************************************************************************
"""
import logging
import os

class Clog(object):

    def __init__(self, conf, names_iterable, path=None):

        if not path:
            path = conf.get('paths', 'PATH_LOGS')
        # Create the containing folder for logs.
        self.create_folder(conf.get('paths', 'PATH_LOGS'))
        self.create_folder(path)

        # create the logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # create the handlers with the received names.
        if isinstance(names_iterable, (tuple, list, set)):

            # evita excepciones por enviar una lista con uno o varios elementos vacios
			# Avoid errors if the iterable is empty or has empty items inside it or duplicates.
            names = set(names_iterable)
            try:
                names.remove('')
            except:
                pass

            formatter = logging.Formatter('%(asctime)s [%(module)s %(funcName)s] %(levelname)s: %(message)s',
                                          '%Y-%m-%d %H:%M:%S')

            for n in names:
                handler = logging.FileHandler(os.path.join(path, n))
                handler.setFormatter(formatter)
                if 'INFO' in n:
                    handler.setLevel(logging.INFO)
                elif 'DEBUG' in n:
                    handler.setLevel(logging.DEBUG)
                elif 'ERROR' in n:
                    handler.setLevel(logging.ERROR)

                logger.addHandler(handler)
            # logger finished
            self.logger = logger
        else:
            raise AttributeError('The parameter name_iterable must be iterable.')

    def create_folder(self, folder):
        """
        Checks if the received folder exists, and otherwise creates it.
        """

        try:
            os.listdir(folder)
        except OSError:
            os.makedirs(folder)
