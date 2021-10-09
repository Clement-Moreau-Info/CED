from enum import Enum
from typing import List

##
# Different edit operations
##
class Edit(Enum):
    MOD = 1
    ADD = 2
    DEL = 3

##
# Contextual Edit Operation
#
# op        : Edit operation performed
# x         : New symbol edited
# k_edit    : position of edition (in [1, len(S_i)]) 
# S_i       : Sequence of symbols
##
class Cxt_edit:
    def __init__(self, op: Edit, x: str, k_edit: int, S_i: List[str]):
        self.op = op
        self.x = x
        self.k_edit = k_edit - 1 # Begin at 0
        self.S_i = S_i
