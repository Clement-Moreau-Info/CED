from enum import Enum
from typing import List, TypeVar

# To be generic
T = TypeVar('T')

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
class CxtEdit:
    def __init__(self, op: Edit, x: T, k_edit: int, seq_i: List[T]):
        self.op = op
        self.x = x
        self.k_edit = k_edit - 1
        self.seq_i = seq_i
