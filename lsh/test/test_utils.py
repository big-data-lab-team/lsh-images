import itertools
import warnings
import math

import numpy as np

from .. import utils

def test_unit_vector():
    # make random vector. get unit vector. check euclid distance = 1 and cosine dist to original = 0
    pass

def test_muller_generation_with_given_seed():
    expected = [ 0.17595171871347956, -0.13194366540433328,  0.9693375432538666, -0.10052874038049053, 0.043709969543711376 ]
    hp = utils.muller_generate_vector(seed=5, dim=5)
    for a, b in zip(expected, hp):
        assert a == b


def test_muller_generation_generates_unit_vectors():
    seeds = utils.generate_random_seeds(1000)
    for i in range(len(seeds)):
        hp = utils.muller_generate_vector(seeds[i], 100)

        for a, b in zip(hp, hp / np.linalg.norm(hp)):
            assert round(a, 8) == round(b, 8)


def test_cosine_distance():
    dim = 100
    vq = 1000 # vector quant
    max_val =  100
    min_val = -100
    q = np.random.randint(min_val, max_val, size=dim)
    vecs = np.random.randint(min_val, max_val, size=(vq, dim))
    average = 0.0
    for v in vecs:
        sim = utils.cosine_similarity(v, q)
        average += sim
        assert sim <= 1 and sim >= -1
    average /= vq
    print("average", average)
    print("ratio:", average * math.sqrt(dim))
    assert average * math.sqrt(dim) > 0.7 and average * math.sqrt(dim) < 0.9


def test_perturb_vector():
    dim = 100
    vq = 1000 # vector quant
    max_val =  100
    min_val = -100
    q = np.random.randint(min_val, max_val, size=dim)
    vecs = np.random.randint(min_val, max_val, size=(vq, dim))
    for v in vecs:
        rand_dist = np.random.randint( dim * max_val / 16)
        perturbed = utils.perturb_vector(q, rand_dist)
        act_dist = np.linalg.norm(q - perturbed)
        assert act_dist <= rand_dist + 1 and act_dist >= rand_dist - 1
