import sys
from os.path import expanduser, join, exists, dirname
from pprint import pprint
from fabric.api import task

import default_settings


def import_module(name, package=None):
    __import__(name)
    return sys.modules[name]

class Settings(object):
    """
    Settings object inspired by django.conf.settings.
    """
    def __init__(self):
        self._apply_settings_from_module(default_settings)
        custom_settings = import_module('awsfab_settings')
        self._apply_settings_from_module(custom_settings)

    def _apply_settings_from_module(self, settings_module):
        for setting in dir(settings_module):
            if setting == setting.upper():
                setattr(self, setting, getattr(settings_module, setting))

    def as_dict(self):
        """
        Get all settings (uppercase attributes on this object) as a dict.
        """
        dct = {}
        for attrname, value in self.__dict__.iteritems():
            if attrname.upper() == attrname:
                dct[attrname] = value
        return dct

    def pprint(self):
        """
        Prettyprint the settings.
        """
        pprint(self.as_dict())

    #def get_key_filenames(self, key_name):
        #"""
        #Search for ``<key_name>.pem`` in awsfab_settings.KEYPAIR_PATH, and return a
        #list of all of the files we find.
        #"""
        #filenames = []
        #for dirpath in self.KEYPAIR_PATH:
            #filename = join(expanduser(dirpath), key_name) + '.pem'
            #if exists(filename):
                #filenames.append(filename)
        #return filenames

awsfab_settings = Settings()



@task
def print_settings():
    """
    Pretty-print the settings as they are seen by the system.
    """
    awsfab_settings.pprint()



@task
def print_default_settings():
    """
    Print ``default_settings.py``.
    """
    path = join(dirname(default_settings.__file__), 'default_settings.py')
    print open(path).read()
