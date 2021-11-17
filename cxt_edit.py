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


class CxtEdit:   
    def __init__(self, op: Edit, x: T, k_edit: int, seq_i: List[T]):
        """
        :param op:      Edit operation (MOD, ADD, DEL)
        :param x:       Edited symbol
        :param k_edit:  Edited index in the sequence seq_i
        :param seq_i:   Edited sequence
        """
        self.op = op
        self.x = x
        self.k_edit = k_edit - 1
        self.seq_i = seq_i
