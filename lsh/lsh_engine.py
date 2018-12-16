import sys
import datetime
import warnings
import json

import numpy as np

from . import utils

class engine:
    # interface for an lsh engine, aka an LSH function family.

    def __init__(self, dim, seeds=[]):
        if dim < 1:
            raise ValueError('engine\'s dimension parameter cannot be less than 1.')
            sys.exit(0)
        self.dim = dim
        self.seeds = seeds  # seed(s) for each function
        self.python_version = str(sys.version_info[:2])
        self.np_version = np.__version__

    def __str__(self):
        return str(self.get_settings())

    def setup(self, q, dist, k):  # make a structure around q
        pass

    def hash(self, v):
        if len(self.seeds) == 0:
            raise ValueError("No seeds stored in this engine!")
        if self.dim is None:
            raise ValueError("This engine has no dimension set!")

    def get_settings(self):
        return self.__dict__

    def load_settings(self, js):
        if js['python_version'] != str(sys.version_info[:2]):
            warnings.warn('Warning: This LSH struct was generated in python ' +
                    js['python_version'] + ' whereas you\'re on ' \
                    + str(sys.version_info[:2]) + ', you probably want' \
                    'to verify that nothing has changed that may affect' \
                    ' the random generator.')

        if js['np_version'] != str(np.__version__):
            warnings.warn('Warning: This LSH struct was generated with numpy ' +
                    js['np_version'] + ' whereas you\'re on '\
                    + np.__version__ +', you probably want to verify that ' \
                    'nothing has changed that may affect the random generator.')
        self.seeds = js['seeds'].copy()

    def save_settings(self, filename=None):
        if filename is None:
            filename = ('lsh_settings_' + str(datetime.datetime.now()) + '.txt')
        with open(filename, 'w') as f:
            json.dump(self.get_settings(), f)
        f.close()

    def load_settings_file(self, filename):
        with open(filename) as f:
            js = json.load(f)
            self.load_settings(js)
        f.close()
