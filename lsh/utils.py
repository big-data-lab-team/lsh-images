import numpy as np
from random import gauss, randrange

def unit_vector(v):
    return v/np.linalg.norm(v)


def euclidean_dist(v1, v2):
    return np.linalg.norm(v1-v2)


def euclidean_similarity(v1, v2):
    euclid_sim = 1 / (1 + euclidean_dist(v1, v2))

    if euclid_sim > 1:  # occasional misshap from python's floating points
        euclid_sim = 1
    elif euclid_sim < -1:
        euclid_sim = -1


def cosine_similarity(v1, v2):
    cosine_similarity = abs(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    if cosine_similarity > 1:  # occasional misshap from python's floating points
        cosine_similarity = 1
    elif cosine_similarity < -1:
        cosine_similarity = -1

    return cosine_similarity


def generate_random_seeds(quant: int, seed=None):
    np.random.seed(seed)
    return np.random.randint(2**32-1, size=quant).tolist()


def muller_generate_vector(seed: int, dim: int):
    # The generation of random vectors from
    # 'A Note on a Method for Generating Points Uniformly
    # on N-Dimensional Spheres', by Muller et al., 1959

    np.random.seed(seed)
    deviates = np.random.normal(0, 1, size=[dim])
    radius = sum(deviates**2) ** .5
    return (deviates/radius).T


def perturb_vector(v, euclidean_distance, maximum=None):
    # perturbs a vector to a new vector with a particular euclidian distance to the original vector
    if maximum is None:
        maximum = np.max(v)
    minimum = np.min(v)
    perturbed = v.copy()
    dist = 0
    while(dist < euclidean_distance - 2):
        dist = np.linalg.norm(v - perturbed)
        true_max = min( round(euclidean_distance - dist), maximum)
        i = np.random.randint(len(v))
        rand_val = np.random.randint(0, true_max + 1)
        sign = -np.sign(v[i])
        perturbed[i] += sign * rand_val

        if perturbed[i] < minimum:
            perturbed[i] = minimum
        elif perturbed[i] > maximum:
            perturbed[i] = maximum
        if dist > euclidean_distance:
            # if pertrubed too much, restart. Maybe this is bad for really big vectors, find better way of handling this.
            perturbed = v.copy()

    return perturbed


def orthog_projection(v1, v2):
    # orthogonal projection of v1 onto a straight line parallel to v2
    return np.dot(v1, (v2 / np.linalg.norm(v2))) * v2


def random_rot(dim: int, seed: int, dtype='d'):
        # Returns a random rotation matrix in dimension d
        # Code adapted from MDP-toolkit's random_rot(), but using numpy functions instead.
        # The algorithm is described in the paper
        # Stewart, G.W., "The efficient generation of random orthogonal
        # matrices with an application to condition estimators", SIAM Journal
        # on Numerical Analysis, 17(3), pp. 403-409, 1980.
        # For more information see
        # http://en.wikipedia.org/wiki/Orthogonal_matrix#Randomization
        np.random.seed(seed)

        H = np.identity(dim)
        D = np.ones(dim)
        for n in range(1, dim):
            x = np.random.normal(size=(dim-n+1,)).astype(dtype)
            D[n-1] = np.sign(x[0])
            x[0] -= D[n-1]*np.sqrt((x*x).sum())
            Hx = ( np.identity(dim-n+1, dtype=dtype)
                   - 2.* np.outer(x, x)/(x*x).sum() )
            mat = np.identity(dim, dtype=dtype)
            mat[n-1:, n-1:] = Hx
            H = np.dot(H, mat)
        D[-1] = (-1)**(1-dim%2)*D.prod()
        H = (D*H.T).T
        return H


def apply_random_rotation_on_cp(seed, cp, dim=None):
    # Apply random_point_rotation with the same seed on all points of a
    # given cross polytope.
    if dim is None:
        dim = self.dim

    random_rotation_matrix = utils.random_rot(dim, seed)
    apply_rotation_on_cp(cp, random_rotation_matrix)


def apply_rotation_on_cp(cp, rotation_matrix):
    # apply given rotation on a particular cross polytope
    for point in range(len(cp)):
        cp[point] = np.dot(rotation_matrix, cp[point].T)


def generate_cp(radius, dim):
    # Generate the "original" or "default" cross polytope on given,
    # dimensions and radius, aka [[radius, 0, 0, ...], [0, radius, 0, 0, ...] ... [-radius, 0, 0, 0 ...] ...]
    # Each row is a different point.

    points = np.ndarray(shape=[2*dim, dim])
    first_point = np.array([0] * dim)
    first_point[0] = radius
    points[0, :] = first_point
    i = 0
    val = radius
    for point in range(1, dim*2):
        first_point[i] = 0
        i += 1
        if i == dim:
            val = -radius
            i = 0
        first_point[i] = val
        points[point, :] = first_point
    return np.array(points)


# gram schmidt process. from stack overflow.
def _gs_cofficient(v1, v2):
    return np.dot(v2, v1) / np.dot(v1, v1)

def _multiply(cofficient, v):
    return list(map((lambda x : x * cofficient), v))

def _proj(v1, v2):
    return _multiply(_gs_cofficient(v1, v2) , v1)

def gramm_schmidt_process():
    Y = []
    for i in range(len(X)):
        temp_vec = X[i]
        for inY in Y :
            proj_vec = _proj(inY, X[i])
            temp_vec = list(map(lambda x, y : x - y, temp_vec, proj_vec))
        Y.append(temp_vec)
    return Y

