import itertools

import numpy as np

from ..lsh_hp_engine import hyperplane_engine
from . import test_engine
from .. import utils

from ..lsh_cp_engine import cp_engine


#def test_verify_generate_cp():
#    dim = 3
#    c = cp_engine(3, None)
#    # a cross polytope of dimension 3, with a radius of 5
#    true_cp = np.array([[5,0,0],[0,5,0],[0,0,5],[-5,0,0],[0,-5,0],[0,0,-5]])
#    for true_row, act_row in zip(true_cp, utils.generate_cp(5, dim)):
#        for true_el, act_el in zip(true_row, act_row):
#            assert true_el == act_el
#
#def _verify_rotations_helper(points):
#    # return distance of all points from each other and from the origin
#    from_each_other = []
#    from_origin = []
#
#    for i in list(itertools.combinations(points,2)):
#        from_each_other.append(utils.euclidean_dist(i[0], i[1]))
#
#    for i in range(len(points)):
#        from_origin.append(utils.euclidean_dist( [0] * len(points[0]), points[i]))
#    return [from_each_other, from_origin]
#
#def test_verify_cp_rotation():
#    # generate a default cp. get distances. rotate it, check if distances are the same.
#    dim = 3
#    c = cp_engine(dim, None)
#    cp = utils.generate_cp(5, dim)
#    dists_before_rotation = _verify_rotations_helper(cp)
#    cp = c.apply_random_rotation_on_cp(1789, cp)
#    dists_after_rotation  = _verify_rotations_helper(cp)
#
#    for dists_b, dists_a in zip(dists_before_rotation, dists_after_rotation):
#        for dist_b, dist_a in zip(dists_b, dists_a):
#            assert round(dist_b, 8) == round(dist_a, 8)
