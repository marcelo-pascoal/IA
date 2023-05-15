from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()
        self._lines_goal_matrix = None
        self._cols_goal_matrix = None

    # Calcula a disatncia Manhattan desde a localização do forklift até aos goal
    def compute(self, state: WarehouseState) -> float:
        self._lines_goal_matrix = abs(state.goal_line - state.line_forklift)
        self._cols_goal_matrix = abs(state.goal_col - state.column_forklift)
        return self._lines_goal_matrix + self._cols_goal_matrix

    def __str__(self):
        return "Tiles distance to next goal"
