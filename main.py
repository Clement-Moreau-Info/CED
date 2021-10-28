from ced import *
import networkx as nx
from functools import lru_cache, partial
import pandas as pd
import multiprocessing as mp


def trivial(x: T, y: T) -> float:
    return 1 if x != y else 0


@lru_cache(maxsize=100000)
def wu_palmer(x: str, y: str, onto: nx.DiGraph, rootnode="All") -> float:
    return (2.0 * nx.shortest_path_length(onto, rootnode, nx.lowest_common_ancestor(onto, x, y))) / (
            nx.shortest_path_length(onto, rootnode, x) + nx.shortest_path_length(onto, rootnode, y))


##
# Extraction of all semantic sequences from a file .csv
# path : path of the file
# sep  : separator
# id   : id sequence colonne
##
def extract_seq(path: str, sep=";", id="id") -> List[List[str]]:
    df = pd.read_csv(path, sep=sep)
    max_seq = max(df[id]) + 1
    return [[x for x in df[df[id] == i].iloc[:, 1].values.tolist()]
            for i in range(1, max_seq)]


def main():
    # Path to ontology
    path_onto = "ontology_sac.txt"
    ontology = nx.read_adjlist(path_onto, create_using=nx.DiGraph)

    seq1 = ['1', '7', '1', '11', '2', '5', '2', '9']
    seq2 = ['1', '10', '1', '7', '3', '10']

    # Extract sequences
    seq = extract_seq("test_seq.csv")

    e = CxtEdit(Edit.MOD, '8', 4, seq1)
    nu = temporal_vec(e, 4)
    print(nu)
    print("CED(seq1, seq2) = ", ced(seq1, seq2, partial(wu_palmer, onto=ontology), 4))


if __name__ == '__main__':
    main()
