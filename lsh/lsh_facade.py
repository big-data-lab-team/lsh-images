import numpy as np

from .lsh_engine            import engine
from .lsh_hp_engine         import hyperplane_engine
from .lsh_smart_hp_engine   import smart_hp_engine
from .lsh_cp_engine         import cp_engine
from .                      import utils

#TODO: fix file name vs class name issue for most engines
#TODO: add profiler to find out what made the hyperplane engines suddenly take way longer than before. cprofile, or profilestats, a wrapper on cprofile

class facade_builder():
    def __init__(self):
        self.dim    = None # dimension of vectors
        self.dist   = None # max euclidean distance to q before being hashed to a different bucket, R
        self.engine = None # type of engine used for hashing. Can be
                           # hyperplane, smart_hyperplane, or cross_polytope
        self.k      = None # number of functions per family
        self.l      = None # number of families. If a of them
                           # get a hash hit, accept.
        self.a = 1         # How many tables are needed to accept the vector as near neighbour. Defaults to 1.

    def with_dim(self, dim):
        if dim <= 0:
            raise ValueError('Dimension must be greater than 0!')
        self.dim = dim
        return self

    def with_dist(self, dist):
        if dist <= 0:
            raise ValueError('Distance must be greater than 0!')
        self.dist = dist
        return self

    def with_engine(self, engine):
        if engine != 'hyperplane' and engine != 'cross_polytope' and \
                engine != 'smart_hyperplane':
            raise ValueError('Engine must be hyperplane, ' \
                    'smart_hyperplane, or cross_polytope!')
        self.engine = engine
        return self

    def with_k(self, k):
        if k <= 0:
            raise ValueError('k must be greater than 0!')
        self.k = k
        return self

    def with_l(self, l):
        if l <= 0:
            raise ValueError('l must be greater than 0!')
        self.l = l
        return self

    def with_a(self, a):
        if a <= 0:
            raise ValueError('a must be greater than 0!')
        self.a = a
        return self

    def build_struct(self):
        if self.dim is None or self.dist is None or self.engine is None \
                or self.k is None or self.l is None or self.a is None:
            raise ValueError('Invalid structure. Check you have given' \
                    ' all necessary parameters.')
        return facade(self.dim, self.dist, self.engine, self.k, self.l, self.a)

    def load_facade(filename):
        pass

class facade():
    def __init__(self, dim, dist, engine, k, l, a):
        self.dim    = dim
        self.dist   = dist
        self.engine = engine
        self.k      = k
        self.l      = l

        self.tables   = []
        self.q_hashes = []
        self.a = a

    def load_engine(self, json_dict=None):
        e = None
        if self.engine == 'hyperplane':
            e = hyperplane_engine(self.dim)
        elif self.engine == 'smart_hyperplane':
            e = smart_hp_engine(self.dim, dist=self.dist)
        elif self.engine == 'cross_polytope':
            e = cp_engine(self.dim)

        if json_dict is not None:
            e.load_settings(json_dict)
        return e

    def setup(self, q, dist=None, k=None):
        if dist is None:
            dist = self.dist
        if k is None:
            k = self.k
        print('Setting up engines...')
        for i in range(self.l):
            e = self.load_engine()
            e.setup(q, self.dist, self.k)
            self.q_hashes.append(e.hash(q))
            self.tables.append(e.get_settings())
        print('Done.')

    def hash(self, v):
        if self.l == 0:
            raise ValueError('No engines on this facade!')

        v_hashes = []
        for settings in self.tables:
            v_hashes.append(self.load_engine(settings).hash(v))
        return v_hashes

    def is_near_neighbour(self, v, a=None):
        if a is None:
            a = self.a

        v_hashes = self.hash(v)
        count = 0
        for i in range(len(v_hashes)):
            if v_hashes[i] == self.q_hashes[i]:
                count += 1
        return count >= a
