import numpy as np
import random
import math

from ..lsh_smart_hp_engine import smart_hp_engine
from . import test_engine
from .. import utils
from ..lsh_facade import facade_builder, facade

# for graphing of vector acceptance / rejection
try:
    from plotly import tools
    import plotly.offline as py
    import plotly.graph_objs as go
    graphing = True
except ImportError:
    graphing = False


#def test_on_actual_image():
#    hash_accuracy(100, 100, 'smart_hyperplane', 10, 5, 1000)

#def test_naive_hp_engine():
#    print('\n\nTesting naive hyperplane engine.')
#    _hash_accuracy_helper(10, 50, 'hyperplane', 5, 10, 1000)

#def test_smart_hp_engine():
#    print('\n\nTesting smarter hyperplane engine.')
#    _hash_accuracy_helper(50, 50, 'smart_hyperplane', 3, 20, 1000)

def test_cp_engine():
    print('\n\nTesting cross polytope engine.')
    _hash_accuracy_helper(50, 100, 'cross_polytope', 10, 1, 1000)

def _hash_accuracy_helper(dim, dist, engine, k, l, candidate_quant, q=None, max_val=None):
    #TODO: make this into a class
    if max_val is None:
        max_val = 100
    if q is None:
        q = np.random.randint(-max_val, max_val, size=dim)
    builder = facade_builder()
    f = builder.with_dim(dim).with_dist(dist).with_engine(engine).with_k(k).with_l(l).with_a(1).build_struct()

    f.setup(q, dist, k)

    print('Vectors with euclidean distances of:', 0, 'to' , dist)
    under = _inner_helper(f, q, _generate_vectors_helper(candidate_quant, q, 0, dist), dist)
    print('Vectors with euclidean distances of:', dist + 1, 'to', 10 * dist)
    over = _inner_helper(f, q, _generate_vectors_helper(candidate_quant, q, dist + 1, 10*dist), dist)
    if graphing:
        nn_dists = []
        nnn_dists = []
        nn_dists.extend(under[0])
        nn_dists.extend(over[0])
        nnn_dists.extend(under[1])
        nnn_dists.extend(over[1])
        graph(nn_dists, nnn_dists, candidate_quant, engine)


def _inner_helper(f, q, vectors, dist):
    # helper func for testing hash functions on specific vectors
    print('generated.')
    false_negatives = 0
    false_positives = 0
    near_neighbour_dists = []
    not_near_neighbour_dists = []
    for v in vectors:
        is_near_neighbour = f.is_near_neighbour(v, 1)
        actual_dist = utils.euclidean_dist(v, q)
        if is_near_neighbour:
            near_neighbour_dists.append(actual_dist)
        else:
            not_near_neighbour_dists.append(actual_dist)

        if not is_near_neighbour and actual_dist <= dist:
            false_negatives += 1
        elif is_near_neighbour and actual_dist > dist:
            false_positives += 1

    print('Out of', len(vectors), 'reported', false_negatives,\
        '\tfalse negatives and', false_positives, '\tfalse positives.')
    if graphing:
        return [near_neighbour_dists, not_near_neighbour_dists]


def _generate_vectors_helper(candidate_quant, q, min_dist, max_dist):
    vs = []
    for i in range(candidate_quant):
        random_dist = random.randint(min_dist, max_dist)
        vs.append(utils.perturb_vector(q, random_dist))
    return vs


def graph(nn_dists, nnn_dists, length, engine):
    x = list(range(1, len(nn_dists)))
    nn = go.Scatter(x=x, y=nn_dists, mode='markers', marker = dict(color = 'green'), name='nn')
    x = list(range(len(nn_dists) + 1, len(nn_dists) + 1 + len(nnn_dists)))
    nnn = go.Scatter(x=x, y=nnn_dists, mode='markers', marker = dict(color = 'red'), name='not nn')
    data = [nn, nnn]
    py.plot({'data': data,'layout':{'title': engine,'font': dict(size=16)}}, filename='testing_engines.html')

