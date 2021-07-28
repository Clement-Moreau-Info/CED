
from cxt_edit import *
from ced import *
import networkx as nx
from functools import lru_cache
import pandas as pd
import multiprocessing as mp

# Path to ontology
path_onto = "ontology_sac.txt"
ontology = nx.read_adjlist(path_onto, create_using=nx.DiGraph)


def trivial(x: str, y: str) -> float:
    return 1 if x != y else 0


@lru_cache(maxsize=100000)
def wu_palmer(x: str, y: str, rootnode="All", onto=ontology) -> float:
    return (2.0 * nx.shortest_path_length(onto, rootnode, nx.lowest_common_ancestor(onto, x, y))) / (
            nx.shortest_path_length(onto, rootnode, x) + nx.shortest_path_length(onto, rootnode, y))


# Define the similarity used
def sim(x: str, y: str) -> float:
    return wu_palmer(x, y)


if __name__ == '__main__':
    S1 = ['1', '7', '1', '11', '2', '5', '2', '9']
    S2 = ['1', '10', '1', '7', '3', '10']
    # e = Cxt_edit(Edit.MOD, '8', 4, S1)
    # nu = temporal_vec(e, 4)
    # print(nu)
    print("CED(S1,S2) = ", ced(S1, S2, sim, 4))
