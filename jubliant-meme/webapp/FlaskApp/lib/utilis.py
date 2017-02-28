#!/usr/bin/env python

import os
import ConfigParser


class Utilities(object):
    @classmethod
    def parseConfiguration(cls, ini):
        """ Parse the config contents of secretfile
        """
        options = {}
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        try:
            config.read(ini)
            for section in config.sections():
                for option in config.options(section):
                    options[option] = config.get(section, option)
        except Exception as err:
            raise Exception(err)

        return options
