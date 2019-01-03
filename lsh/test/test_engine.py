import os
import random
import itertools
import warnings
import math

import numpy as np

from ..lsh_engine import engine
from .. import utils


def test_save_settings_in_file_should_pass():
    e = engine(dim=5, seeds=[5,7,9])
    e.save_settings('lsh_settings.json')

    os.remove('lsh_settings.json')


def test_save_and_load_settings_in_file_should_pass():
    e = engine(dim=5, seeds=[5,7,9])
    e.save_settings('lsh_settings.json')

    f = engine(dim=5)
    f.load_settings('lsh_settings.json')

    assert all([s1 == s2 for s1, s2 in zip(e.get_settings(), f.get_settings())])
    os.remove('lsh_settings.json')


#def lsh_quality_tester(e, dim, function_quantity, vec_quantity, max_dist, q=None):
#    # This shouldn't be used by the interface but by implementations of the engine.
#    max_val = 100
#
#    if q is None:
#        q = np.random.randint(max_val, size=dim)
#    # random vectors
#    rando_vs = np.random.randint(max_val, size=(vec_quantity, dim))
#    # vectors purposely close to but smaller than given euclidean distance
#    small_vs = []
#    for i in range(vec_quantity):
#        random_dist = random.randint(max_dist - round(max_dist/100) - 5, max_dist)
#        small_vs.append(utils.perturb_vector(q, random_dist))
#
#    # vectors purposely close to but larger than given euclidean distance
#    large_vs = []
#    for i in range(vec_quantity):
#        random_dist = random.randint(max_dist + 1, max_dist + round(max_dist/100) + 5)
#        large_vs.append(utils.perturb_vector(q, random_dist))
#    print('max dist is:', max_dist)
#    print('testing random vectors')
#    _helper_lsh_qt(e, q, rando_vs, max_dist)
#    print('testing vectors with euclidean distances of:', max_dist - round(max_dist/100) - 5, 'to' ,max_dist)
#    _helper_lsh_qt(e, q, small_vs, max_dist)
#    print('testing vectors with euclidean distances of:', max_dist + 1, 'to', max_dist + round(max_dist/100) + 5)
#    _helper_lsh_qt(e, q, large_vs, max_dist)
#
#
#def _helper_lsh_qt(e, q, vectors, max_dist):
#    # helper func for testing hash functions on specific vectors
#    q_hash = e.hash(q)
#    false_negatives = 0
#    false_positives = 0
#    for v in vectors:
#        v_hash = e.hash(v)
#        actual_dist = utils.euclidean_dist(v, q)
#        #print(actual_dist, '\t', v_hash)
#        if v_hash != q_hash and actual_dist < max_dist:
#            false_negatives += 1
#        if v_hash == q_hash and actual_dist > max_dist:
#            false_positives += 1
#
#    print('Out of', len(vectors), 'reported', false_negatives,\
#            '\tfalse negatives and', false_positives, '\tfalse positives.')
