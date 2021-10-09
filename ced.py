import skfuzzy as fuzz
from cxt_edit import *
import numpy as np
from numba import prange
from typing import Callable, TypeVar

##
# Temporal vector 
#
# e     : Contextual edit operation
# beta  : Boundary of the fuzzy function
##
def temporal_vec(e: Cxt_edit, beta: int) -> List[float]:
    # Defined a fuzzy encoding function (+ 1 to ensure non empty interval)
    mu = fuzz.trapmf(np.arange(0, len(e.S_i)+1),
                     [e.k_edit - beta, e.k_edit, e.k_edit, e.k_edit + beta])
    if e.op == Edit.MOD:
        return mu[:-1] # disregard the + 1
    if e.op == Edit.ADD:
        return [mu[i] if i < e.k_edit else
                (mu[e.k_edit - 1] if i == e.k_edit else mu[i + 1])
                for i in range(len(e.S_i))]
    else:
        return [mu[i] if i != e.k_edit else 0 for i in range(len(e.S_i))]

##
# Gamma cost function  
#
# e     : Contextual edit operation
# sim   : Similarity between symbol
# beta  : Boundary of the fuzzy function
##
def gamma_cost(e: Cxt_edit, sim: Callable[[str, str], float], beta: int) -> float:
    nu = temporal_vec(e, beta)
    ctx_vector = [sim(e.S_i[k], e.x) * nu[k] for k in range(len(e.S_i))]
    return 1 - max(ctx_vector)

##
# One sided CED. Computation by dynamic programming
#
# S1    : Semantic sequence 1
# S2    : Semantic sequence 2
# sim   : Similarity between symbol
# beta  : Boundary of the fuzzy function
##
def one_sided_ced(S1: List[str], S2: List[str], sim: Callable[[str, str], float], beta: int) -> float:
    dist = np.zeros((len(S1) + 1, len(S2) + 1))
    for i in prange(len(S1) + 1):
        for j in prange(len(S2) + 1):
            if i == 0 or j == 0:
                dist[i, j] = j + i
            else:
                op_mod = Cxt_edit(Edit.MOD, S2[j-1], i-1, S1)
                op_del = Cxt_edit(Edit.DEL, S1[i-1], i-1, S1)
                op_add = Cxt_edit(Edit.ADD, S2[j-1], i-1, S1)

                cost_mod = gamma_cost(op_mod, sim, beta)
                cost_del = gamma_cost(op_del, sim, beta)
                cost_add = gamma_cost(op_add, sim, beta)

                dist[i, j] = round(min(dist[i - 1, j-1] + cost_mod,
                                       dist[i - 1, j] + cost_del,
                                       dist[i, j - 1] + cost_add), 2)
    return dist[len(S1), len(S2)]

##
# CED 
#
# S1    : Semantic sequence 1
# S2    : Semantic sequence 2
# sim   : Similarity between symbol
# beta  : Boundary of the fuzzy function
##
def ced(S1: List[str], S2: List[str], sim: Callable[[str, str], float], beta: int) -> float:
    return max(one_sided_ced(S1, S2, sim, beta), one_sided_ced(S2, S1, sim, beta))
