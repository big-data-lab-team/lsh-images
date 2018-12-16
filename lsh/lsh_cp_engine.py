import sys
import math

import numpy as np
import itertools

from .lsh_engine import engine
from . import utils

class cp_engine(engine):
    def __init__(self, dim, seeds=[]):
        engine.__init__(self, dim, seeds)
        self.radii = []
        self.indexes = []

    def __str__(self):
        return 'cross-polytope engine: ' + str(engine.__str__(self))

    def setup(self, q, dist, k):
        dist = round(dist / 2)
        cp_radius = self._get_max_radius(q, dist)  # Radius of the n-sphere on
                                    # which the cross polytope is inscribed. In the
                                    # first round, it is euclid_dist(query) + dist

        cp_origin = [0]* self.dim   # Origin point of the cross polytope.
                                    # First, it's located at the origin.
                                    # For every round hereafter, it is located
                                    # at one of the previous cross polytope's
                                    # vertices
        seeds       = []
        indexes     = []
        radii       = [cp_radius]

        for i in range(k):
            original_cp     = utils.generate_cp(cp_radius, self.dim)  #TODO: switch dim and radius order of params
            best_cp_point   = None
            best_seed       = None
            best_index      = None
            best_dist       = math.inf

            made_valid_cp = False
            count = 0
            print('\n')
            for attempts in range(200):  # make this a 'tolerance' parameter
                # generate a random cp, move it to the origin given
                cp = original_cp.copy()
                seed = utils.generate_random_seeds(1)[0]
                utils.apply_rotation_on_cp(cp, utils.random_rot(self.dim, seed))
                cp += cp_origin
                # verify cp. If its a good cp, check the distance of the point
                # q is hashed to. if its better than our best cp, keep it
                if self._verify_cp(cp, q, dist, cp_radius - dist):
                    print('GOT ONE')
                    made_valid_cp = True
                    q_hash, cp_dist = self.cp_hash(cp, q)  # note: we already hashed it once, in verify cp. expensive to do it again
                    if cp_dist < best_dist: # is this truly the best cp available? find heuristic for choosing cp
                        best_cp_point = cp[q_hash].copy()
                        best_seed = seed
                        best_index = q_hash
                        best_dist = cp_dist

            if made_valid_cp:
                cp_radius = np.ceil(best_dist + dist)
                seeds.append(best_seed)
                indexes.append(best_index)
                radii.append(cp_radius)
                cp_origin = best_cp_point  # move origin of next cross polytope
            else:
                print('After many attempts, unable to generate any more cp. Halting now')
                break

        self.seeds = seeds
        self.radii = radii
        self.indexes = indexes
        print("Got", len(seeds), "CPs...", radii)

    def _get_max_radius(self, q, dist):
        # aka get the unit vector of the query, extend it by R, then move it to q.
        # Get the euclidean distance of this vector from the origin, this will
        # be the radius of the n-sphere on which the first cross polytope is defined.
        return np.ceil(utils.euclidean_dist(utils.unit_vector(q) * dist + q, [0] * len(q)))

    def cp_hash(self, cp, v):
        min_dist   = math.inf
        hash_point = math.inf
        for i in range(len(cp)):
            dist = utils.euclidean_dist(v, cp[i])
            if dist < min_dist:
                min_dist = dist
                hash_index = i
        return [hash_index, min_dist]

    def hash(self, v):
        # this can definitely be improved, based on same logic as smart hp.
        hashes = []
        origin = [0] * self.dim
        for i in range(len(self.seeds)):
            if utils.euclidean_dist(origin, v) > self.radii[i]:
                return -1
            cp = utils.generate_cp(self.radii[i], self.dim)
            # we only care about the point on which q was hashed to. So, normally, we'd only rotate that point, and check if v is within a set distance to it. If no, we can skip the hashing part altogether.
            utils.apply_rotation_on_cp(cp, utils.random_rot(self.dim, self.seeds[i]))
            cp += origin
            #if utils.euclidean_dist(cp[self.indexes[i]], v) >
            hashes.append(self.cp_hash(cp, v)[0])
            origin = cp[self.indexes[i]]
        return ''.join(map(str, hashes))

    def _verify_cp(self, cp, q, dist, upper_bound):
        # better algo:
        # first, check the distance to the point q is hashed to. Then, for each point on the cp, check the distance between q and that point.
        dists = [utils.euclidean_dist(q, cp[i]) for i in range(len(cp))]
        min_index = dists.index(min(dists))
        min_dist = dists[min_index]
        #if min_dist + dist > upper_bound:  # Normally we'd want this to be true: That is, that the more cps we generate, the smaller they get. But, in higher dimensions, this nearly always ends up failing. As in, nearly all rotations end up with a point hashed with a pretty big euclidean distance to q. Why ?
        #    print('too big')
        #    return False
        for i in range(len(dists)):
            if i == min_index:
                continue
            if dists[i] - dist < min_dist:
                print('R sphere around q not fully in bucket.')
                return False
        return True

    def load_settings(self, js): # override
        engine.load_settings(self, js)
        self.radii = js['radii']
        self.indexes = js['indexes']
