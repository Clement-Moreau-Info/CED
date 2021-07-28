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

## About parameters:

### Beta variable
-------------

Temporal vector is encoded by a fuzzy membership function. Beta variable controls the flateness of this function. 
Beta -> ∞ <=> All symbols in sequences are taken into account in sequences. 
Beta -> 0 <=> Classical edit distance


### Sim function
------------

The sim:Σ x Σ -> [0,1] function defined the similarity between all symbols in the alphabet of sequences Σ. 
Basicaly, we can use the trival distance function. 
The Wu-Palmer similarity function used a knowledge graph (i.e., ontology) for symbol comparison. An example of graph structure is given in the file "ontology_sac.txt". 

