import numpy as np
import sys
import signal
import math

from .lsh_engine import engine
from .lsh_hp_engine import hyperplane_engine
from . import utils

class smart_hp_engine(hyperplane_engine):
    # helper class for finding good hyperplanes.
    def __init__(self, dim, seeds=[], dist=None):
        hyperplane_engine.__init__(self, dim, seeds)
        self.dist = dist
        self.bucket_scalars = []

    def __str__(self):
        return 'smart hyperplane engine: ' + str(engine.__str__(self))

    def setup(self, q, dist, k):
        self.seeds = utils.generate_random_seeds(k)
        self.bucket_scalars = self.generate_bucket_scalars(q, self.seeds, dist)

    #def _try_to_generate_hyperplanes_within_range(self, tries, q, min_euclid_dist, max_euclid_dist):
    #    accepted_seeds = []
    #    seeds = utils.generate_random_seeds(tries)
    #    for i in range(tries):
    #        hp = utils.muller_generate_vector(seeds[i], self.dim)
    #        dist = utils.euclidean_dist(hp, utils.orthog_projection(q, hp))
    #        if dist >= min_euclid_dist and dist <= max_euclid_dist:
    #            accepted_seeds.append(seeds[i])
    #            return accepted_seeds
    #    return accepted_seeds

    #def _generate_good_hyperplanes_for_cosine(self, hq, min_euclid_dist, max_euclid_dist, tolerance):
    #    # min distance: any distance smaller than this will be rejected. Don't want to be too restrictive.
    #    # max distance: any distance larger than this will be rejected. Don't want to be too tolerant.
    #    # Note: The smaller the gap between these two, the harder it will be to find hyperplanes that fit.

    #    print('You may exit out of this function with CTRL+C at any ' \
    #            'time, I will store the currently generated seeds in this engine')
    #    # for catching any attempted kills of the program
    #    signal.signal(signal.SIGINT, signal.default_int_handler)

    #    accepted_seeds = []
    #    try:
    #        got_valid_hp = False
    #        while( not got_valid_hp):
    #            print("Trying range...", min_euclid_dist, max_euclid_dist)
    #            seeds = self._try_to_generate_hyperplanes_within_range(tolerance, min_euclid_dist, max_euclid_dist)
    #            if len(seeds) == 0:
    #                max_euclid_dist += max_euclid_dist/10
    #            else:
    #                got_valid_hp = True

    #        while(len(accepted_seeds) < hq):
    #            seed = self._try_to_generate_hyperplanes_within_range(1, min_euclid_dist, max_euclid_dist)
    #            if len(seed) == 1:
    #                accepted_seeds.append(seed[0])
    #        return accepted_seeds

    #    except KeyboardInterrupt:
    #        self.seeds = accepted_seeds
    #        print('currently accepted seeds:')
    #        print(self.seeds)
    #        self.save_settings()


    def generate_bucket_scalars(self, q, seeds, dist):
        bucket_scalars = []
        for seed in seeds:
            hp = utils.muller_generate_vector(seed, self.dim)

            x = utils.orthog_projection((hp *  math.sqrt(dist)) + q, hp)[0] / hp[0]
            y = utils.orthog_projection((hp * -math.sqrt(dist)) + q, hp)[0] / hp[0]
            if x > y:
                x, y = y, x
            bucket_scalars.append([x, y])
            #outer_x = utils.orthog_projection((hp *  30) + q, hp)[0] / hp[0]
            #outer_y = utils.orthog_projection((hp * -30) + q, hp)[0] / hp[0]
            #inner_x = utils.orthog_projection((hp *  12) + q, hp)[0] / hp[0]
            #inner_y = utils.orthog_projection((hp * -12) + q, hp)[0] / hp[0]

            ## switch so x is always smaller
            #if outer_x > outer_y:
            #    outer_x, outer_y = outer_y, outer_x
            #if inner_x > inner_y:
            #    inner_x, inner_y = inner_y, inner_x

            #bucket_scalars.append([outer_x, outer_y, inner_x, inner_y])
        return bucket_scalars

    def _compare_scalar(self, scalar, i):
        if scalar >= self.bucket_scalars[i][0] and scalar <= self.bucket_scalars[i][1]:
            #if scalar >= self.bucket_scalars[i][2] and scalar <= self.bucket_scalars[i][3]:
                return '1'
            #else:
            #    return '2'
        return '0'

    def hash(self, v):
        scalars = self._project_onto_hyperplanes(v)
        h = ''.join([self._compare_scalar(scalars[i], i) for i in range(len(self.seeds))])
        return h

    def load_settings(self, js): # override
        engine.load_settings(self, js)
        self.bucket_scalars = js['bucket_scalars']
