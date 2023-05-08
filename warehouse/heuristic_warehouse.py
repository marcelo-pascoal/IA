from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()
        self._lines_goal_matrix = None
        self._cols_goal_matrix = None

    def compute(self, state: WarehouseState) -> float:
        if state.catch:
            self._lines_goal_matrix = abs(state.line_product_catch - state.line_forklift) 
            self._cols_goal_matrix = abs(state.column_product_catch - state.column_forklift)
        else:
            self._lines_goal_matrix = abs(state.line_exit - state.line_forklift)
            self._cols_goal_matrix = abs(state.column_exit - state.column_forklift)
        return self._lines_goal_matrix + self._cols_goal_matrix

    def __str__(self):
        return "Tiles distance to next goal"

