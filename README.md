# lsh-images
Experiments with Locality-Sensitive Hashing in 3D/4D images

This library seeks to solve the following: Given a query point q in dimension d, and a eucidean distance R, is it possible to build a structure such that given any point p in d, the structure can return whether or not euclideanDist(q,p) <= R with relatively high probability.


Requires python 3.6+.
Also requires numpy, matplotlib for graphing, nibabel for loading neuroimages, and pytest for tests.

run "pytest -s" to see an example of the code.

I've left some of the experimental stuff that I had removed or not gotten working commented out. This is rather bad practice, but I figured it's more useful to have it whilst the concept is still being developed.

The basic idea is the following: a facade holds l family of k functions each. it will take as parameter an engine type (cross polytope, hyperplane...), some querypoint q, and some distance R, and build a structure to try and answer the above question. It can save the settings for the structure in a json structure, or load up some previously saved structure.

More documentation to follow.
