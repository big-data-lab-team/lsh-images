from ..lsh_hp_engine import hyperplane_engine
from . import test_engine
from .. import utils

def test_save_and_load_settings_in_file_should_pass():
    e = hyperplane_engine(dim=5, seeds=[5,7,9], segment_size = 10)
    e.save_settings('lsh_settings.json')

    f = engine(dim=5)
    f.load_settings('lsh_settings.json')

    assert all([s1 == s2 for s1, s2 in zip(e.get_settings(), f.get_settings())])
    os.remove('lsh_settings.json')


#def test_verify_quality_of_naive_segment_hash():
#    dim = 1000
#    function_quant = 100 # aka k, the number of hyperplanes in this family
#    vector_quant_to_test = 1000
#    distance = 100
#    segment_size = distance
#    e = hyperplane_engine(dim, segment_size=segment_size)
#    e.seeds = utils.generate_random_seeds(function_quant)
#
#    print('\nTesting naive hyperplanes, segment hash:\ndim:', dim, \
#            '\neuclidean distance tested:', distance, '\nsegment_size:', \
#            segment_size, '\nh:', function_quant)
#    test_engine.lsh_quality_tester(e, dim, function_quant, vector_quant_to_test, distance)
#
#
#def test_verify_quality_of_naive_binary_hash():
#    # this is just an example, but obviously using binary hash should get terrible results.
#    dim = 1000
#    function_quant = 100
#    vector_quant_to_test = 1000
#    distance = 100
#
#    e = hyperplane_engine(dim)
#    e.seeds = utils.generate_random_seeds(function_quant)
#    print('\nTesting naive hyperplanes, binary hash:\ndim:', dim, '\nh = ', function_quant)
#    test_engine.lsh_quality_tester(e, dim, function_quant, vector_quant_to_test, distance)
