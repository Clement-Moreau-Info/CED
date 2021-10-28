The Contextual Edit Distance
============================

Used in papers : 

* A contextual edit distance for semantic trajectories
> C Moreau, T Devogele, V Peralta, L Etienne
> Proceedings of the 35th Annual ACM Symposium on Applied Computing, 635-637, 2019

* Learning analysis patterns using a contextual edit distance
> C Moreau, V Peralta, P Marcel, A Chanson, T Devogele
> Design, Optimization, Languages and Analytical Processing of Big Data, 2020

* Methodology for Mining, Discovering and Analyzing Semantic Human Mobility Behaviors
> C Moreau, T Devogele, L Etienne, V Peralta, C de Runz
> arXiv preprint arXiv:2012.04767, 2020

--

# Description of files 

## `cxt_edit.py`

Description of a Contextual Edit Operation. 

For short remember, a contextual edit operation e is a 4-tuple such that : 

`e = (op, x, k_edit, S_i)`

where :

- `op` is an edit operation (Enumeration MOD, ADD, DEL)

- `T:x` is the new symbol 

- `int:k_edit` is the position of edition 

- `List[T]:S_i` is the sequence of symbols

## `ced.py`

Code of the Contextual Edit Distance

### `temporal_vec` function

Signature : `temporal_vec(e: Cxt_edit, beta: int) -> List[float]

where : 
- `e` is a Contextual edit operation

- `beta` is the Boundary of the fuzzy function

This function returns the temporal vector `nu` used in `gamma_cost` function. 

This function uses the [`skfuzzy` package](https://pythonhosted.org/scikit-fuzzy/), please, install it this the command line in your terminal :

`pip install -U scikit-fuzzy`

or in your Anaconda/miniconda terminal

`conda install -c conda-forge scikit-fuzzy`

Computation of each case of the vector is detailled in the thesis page 95-96.


### `gamma_cost` function

Signature : `gamma_cost(e: Cxt_edit, sim: Callable[[str, str], float], beta: int) -> float`

where : 

- `e` is a Contextual edit operation

- `sim` is the similarity between symbols

- `beta` is the Boundary of the fuzzy function

This function computes the equation (5.1) detailled in the thesis. 

### `one_sided_ced` function 

Signature : `one_sided_ced(S1: List[str], S2: List[str], sim: Callable[[str, str], float], beta: int) -> float`

where : 

- `seq1` is the semantic sequence 1

- `seq2` is the emantic sequence 2

- `sim` is the similarity between symbols

- `beta` is the Boundary of the fuzzy function

This function computes the equation (5.2) detailled in the thesis.

/!\ This function is not symmetric /!\

This function is computed using Dynamic Programming (see [Wagned-Fisher algorithm](https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm))

### `ced` function 

Signature : `ced(S1: List[str], S2: List[str], sim: Callable[[str, str], float], beta: int) -> float`

where : 

- `seq1` is the semantic sequence 1

- `seq2` is the emantic sequence 2

- `sim` is the similarity between symbols

- `beta` is the Boundary of the fuzzy function

This function computes the CED distance according the equation (5.3) detailled in the thesis.


## `main.py`

Main file to run. 

This file contains similarity functions like : 

### `wu_palmer` function

Signature : `wu_palmer(x: str, y: str, rootnode="All", onto=ontology) -> float`

where : 

- `x` is the first concept

- `y` is the second concept

- `rootnode` is the root node of the knowledge DAG 

- `onto` is the ontology graph create with networkx library.

This function return the Wu-Palmer similarity between `x` and `y` according to the ontology `onto` and the equation (3.4) in the thesis.


### `extract_seq` function

Signature : `extract_seq(path: str, sep=";", id="id") -> List[List[str]]`

where : 

- `path` is the path to the .csv file of sequences

- `sep` is the separator

- `id` is the name of id column

This function extracts sequences from a .csv file such the example file given `test_seq.csv`.

-------------

## About `beta` parameter

Temporal vector is encoded by a fuzzy membership function. `beta` variable controls the flateness of this function. 

- `beta` -> ∞ <=> All symbols in sequences are taken into account in sequences. 

- `beta` -> 0 <=> Classical edit distance
