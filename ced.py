import skfuzzy as fuzz
from cxt_edit import *
import numpy as np
from numba import prange
from typing import Callable


def temporal_vec(e: CxtEdit, beta: int) -> List[float]:
    """
    :param e:       Contextual edit operation
    :param beta:    Boundary of the fuzzy function
    :return:        Temporal fuzzy vector
    """
    # Defined a fuzzy encoding function (+ 1 to ensure non empty interval)
    mu = fuzz.trapmf(np.arange(0, len(e.seq_i)+1),
                     [e.k_edit - beta, e.k_edit, e.k_edit, e.k_edit + beta])
    if e.op == Edit.MOD:
        return mu[:-1]
    if e.op == Edit.ADD:
        return [mu[k] if k < e.k_edit else
                (mu[e.k_edit - 1] if k == e.k_edit else mu[k + 1])
                for k in range(len(e.seq_i))]
    else:
        return [mu[k] if k != e.k_edit else 0 for k in range(len(e.seq_i))]


def gamma_cost(e: CxtEdit, sim: Callable[[T, T], float], beta: int) -> float:
    """
    :param e:       Contextual edit operation
    :param sim:     Similarity between symbol
    :param beta:    Boundary of the fuzzy function
    :return:        Cost of the edit operation e
    """
    nu = temporal_vec(e, beta)
    ctx_vector = [sim(e.seq_i[k], e.x) * nu[k] for k in range(len(e.seq_i))]
    return 1 - max(ctx_vector)


def one_sided_ced(seq1: List[T], seq2: List[T], sim: Callable[[T, T], float], beta: int) -> float:
    """
    :param seq1:    Semantic sequence 1
    :param seq2:    Semantic sequence 2
    :param sim:     Similarity between symbol
    :param beta:    Boundary of the fuzzy function
    :return:        One-sided CED (edit seq1 to seq2)
    """
    dist = np.zeros((len(seq1) + 1, len(seq2) + 1))
    for i in prange(len(seq1) + 1):
        for j in prange(len(seq2) + 1):
            if i == 0 or j == 0:
                dist[i, j] = j + i
            else:
                op_mod = CxtEdit(Edit.MOD, seq2[j-1], i-1, seq1)
                op_del = CxtEdit(Edit.DEL, seq1[i-1], i-1, seq1)
                op_add = CxtEdit(Edit.ADD, seq2[j-1], i-1, seq1)

                cost_mod = gamma_cost(op_mod, sim, beta)
                cost_del = gamma_cost(op_del, sim, beta)
                cost_add = gamma_cost(op_add, sim, beta)

                dist[i, j] = round(min(dist[i - 1, j-1] + cost_mod,
                                       dist[i - 1, j] + cost_del,
                                       dist[i, j - 1] + cost_add), 2)
    return dist[len(seq1), len(seq2)]


def ced(seq1: List[T], seq2: List[T], sim: Callable[[T, T], float], beta: int) -> float:
    """
    :param seq1:    Semantic sequence 1
    :param seq2:    Semantic sequence 2
    :param sim:     Similarity between symbol
    :param beta:    Boundary of the fuzzy function
    :return:        CED(seq1,seq2)
    """
    return max(one_sided_ced(seq1, seq2, sim, beta), one_sided_ced(seq2, seq1, sim, beta))
