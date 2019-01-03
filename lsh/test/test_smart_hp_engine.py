import numpy as np

from ..lsh_smart_hp_engine import smart_hp_engine
from . import test_engine
from .. import utils

#def test_verify_accuracy_of_smart_hyperplane_cosine():
#    dim = 1000
#    function_quant = 10
#    vector_quant_to_test = 1000
#    distance = 100
#    segment_size = distance
#    q = np.random.randint(100, size=dim)
#    e = smart_hp_engine(dim, q, segment_size=segment_size)
#    # very high tolerance to generate the best hyperplanes
#    e.seeds = e.generate_good_hyperplanes(function_quant, distance, distance + distance/100, 10000)
#
#    print('Testing smart hyperplanes, segment hash, with segments of size 1')
#    test_engine.lsh_quality_tester(e, dim, function_quant, vector_quant_to_test, distance, q)

def test_verify_accuracy_of_smart_hyperplane():
    dim = 100
    function_quant = 100
    vector_quant_to_test = 1000
    distance = 100
    segment_size = distance
    q = np.random.randint(100, size=dim)
    # for smart hp, the segment size should always be the max euclid distance
    e = smart_hp_engine(dim, dist=distance)
    # very high tolerance to generate the best hyperplanes
    e.seeds = utils.generate_random_seeds(function_quant)
    e.bucket_scalars = e.generate_bucket_scalars(q, e.seeds)

    print('\nTesting smart hyperplanes:\ndim:', dim, \
            '\neuclidean distance tested:', distance, '\nh:', function_quant)
    test_engine.lsh_quality_tester(e, dim, function_quant, vector_quant_to_test, distance, q)
