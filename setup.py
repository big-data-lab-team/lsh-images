from setuptools import setup

VERSION = '0.0.1'
DEPS = ['numpy']

setup(
    name='lsh',
    package=find_packages(),
    version=VERSION,
    license='GPLv3',
    description='Locality-Sensitive Hashing in 3D/4D images',
    long_description=open('README.md').read(),
    author='Anne-Laure Ehresmann',
    url='https://github.com/big-data-lab-team/lsh-images',
    packages=['lsh'],
    test_suite='pytest',
    tests_require=['pytest'],
    install_requires=DEPS,
    zip_safe=False
)
