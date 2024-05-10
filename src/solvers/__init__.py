from ._heap_solvers import a_star, greedy, uniform_cost
from ._ida_star import ida_star
from ._incremental import incremental

SOLVERS = [incremental, a_star, greedy, uniform_cost, ida_star]
