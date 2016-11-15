#!usr/bin/python
# -*- coding:utf-8 -*-
"""
***********************************************************************************************************************
										files_directories_utilities.py

It contains the various functions that operates within the files or folders inside a project.

***********************************************************************************************************************
"""
import os, shutil, pdb
from datetime import datetime

def create_temporary_folder(log, path):
    """
    Creates the received path. In case it exists, it's removed first.
    """
    if os.path.exists(path):
        delete_temporary_folder(log, path)
    os.mkdir(path, 0755)
    log.debug('Folder %s created' % path)

def delete_temporary_folder(log, path):
    """
    Removes the received path.
    """
    shutil.rmtree(path=path, ignore_errors=True)
    log.debug('Folder %s removed' % path)

def _tounicode(item):
	"""
	Converts the received item (str, unicode, list ...) into unicode.
	"""
    if item is None:
        return u''
    elif isinstance(item, list):
        list_unicodes = []
        for i in item:
            list_unicodes.append(_tounicode(i))
        return list_unicodes
    else:
        if not isinstance(item, unicode):
            str_item = str(item)
            try:
                return str_item.decode('utf-8')
            except:
                pass

            try:
                return str_item.decode('latin-1')
            except:
                pass

            try:
                return str_item.decode('ascii')
            except:
                pass
            # It didn't worked
            return item
        else:
            return item
