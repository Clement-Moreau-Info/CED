from enum import Enum
from typing import List


class Edit(Enum):
    MOD = 1
    ADD = 2
    DEL = 3


class Cxt_edit:
    def __init__(self, op: Edit, x: str, i_edit: int, S_i: List[str]):
        self.op = op
        self.x = x
        self.i_edit = i_edit - 1
        self.S_i = S_i