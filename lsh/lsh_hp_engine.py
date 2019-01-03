import os
import sys
import math
import datetime
import warnings
from random import gauss

import numpy as np

from .lsh_engine import engine
from . import utils


# a naive hyperplane engine. Can do hashing for both cosine dist and euclidean dist.
class hyperplane_engine(engine):
    def __init__(self, dim, seeds=[], segment_size=None):
        engine.__init__(self, dim, seeds)
        self.segment_size = segment_size

    def __str__(self):
        return 'hyperplane engine: ' + str(engine.__str__(self))

    def setup(self, q, dist, k):
        self.segment_size = dist
        self.seeds = utils.generate_random_seeds(k)

    def _project_onto_hyperplanes(self, v):
        # returns the scalar of multiplication by each hyperplane needs to be
        # multipled to obtain v's projection onto them
        scalars = [0] * len(self.seeds)
        for i,seed in enumerate(self.seeds):
            hp = utils.muller_generate_vector(seed, self.dim)
            # extract the scalar of the projection of v onto hp
            scalars[i] = utils.orthog_projection(v, hp)[0] / hp[0]
        return scalars

    def binary_hash(self, v):
        # for cosine distance
        return ''.join([str(int(scalar >=0)) for scalar \
            in self._project_onto_hyperplanes(v)])

    def segment_hash(self, v):
        # for euclidean distance
        if self.segment_size is None:
            raise ValueError('no segment size has been set.')
        return ''.join([str(math.floor(scalar / self.segment_size)) for scalar \
                in self._project_onto_hyperplanes(v)])

    def hash(self, v):  # override
        if len(self.seeds) == 0:
            raise ValueError('no hyperplanes in lsh engine!')

        if len(v) != self.dim:
            raise ValueError('You must use hyperplanes whose normals are of the'
            + ' same dimension as the vector given!')

        if self.segment_size is None:
            return self.binary_hash(v)
        else:
            return self.segment_hash(v)

    def load_settings(self, js): # override
        engine.load_settings(self, js)
        self.segment_size = js['segment_size']
