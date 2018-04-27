from sage.all import *
from sage.misc import *
#import PyNormaliz as PyNormaliz
import numpy as np
from Init import *

# C subset D
# F_v = facets of C visible from D

C,D = generateInitialConditions(2, 0, 10)

print(C.rays_list())
print(D.rays_list())