from typing import TypeVar

import numpy as np
import copy
import constants
from agentsearch.agent import Agent
from agentsearch.state import State
from warehouse.cell import Cell
from warehouse.heuristic_warehouse import HeuristicWarehouse
from warehouse.pair import Pair
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch


class WarehouseAgentSearch(Agent):
    S = TypeVar('S', bound=State)

    def __init__(self, environment: S):
        super().__init__()
        self.initial_environment = environment
        self.heuristic = HeuristicWarehouse()
        self.forklifts = []
        self.products = []
        self.exit = None
        self.pairs = []
        for i in range(environment.rows):
            for j in range(environment.columns):
                if environment.matrix[i][j] == constants.FORKLIFT:
                    self.forklifts.append(Cell(i, j))
                elif environment.matrix[i][j] == constants.EXIT:
                    self.exit = Cell(i, j)
                elif environment.matrix[i][j] == constants.PRODUCT:
                    self.products.append(Cell(i, j))

        for a in self.forklifts:
            for p in self.products:
                self.pairs.append(Pair(a, p))

        for i in range(len(self.products) - 1):
            for j in range(i + 1, len(self.products)):
                self.pairs.append(Pair(self.products[i], self.products[j]))

        for p in self.products:
            self.pairs.append(Pair(p, self.exit))

        for a in self.forklifts:
            self.pairs.append(Pair(a, self.exit))

        for pair in self.pairs:
            cell_start = Cell(pair.cell1.line, pair.cell1.column)
            if environment.matrix[cell_start.line][cell_start.column] != constants.FORKLIFT:
                if environment.matrix[cell_start.line][cell_start.column - 1] == constants.EMPTY:
                    cell_start.column -= 1
                else:
                    cell_start.column += 1
            cell_goal = Cell(pair.cell2.line, pair.cell2.column)
            if environment.matrix[cell_goal.line][cell_goal.column] != constants.EXIT:
                if environment.matrix[cell_goal.line][cell_goal.column - 1] == constants.EMPTY:
                    cell_goal.column -= 1
                else:
                    cell_goal.column += 1
            pair_state = copy.deepcopy(environment)
            pair_state.line_forklift = cell_start.line
            pair_state.column_forklift = cell_start.column
            pair_state.goal_line = cell_goal.line
            pair_state.goal_col = cell_goal.column
            problem = WarehouseProblemSearch(pair_state, cell_goal)
            solution = Agent.solve_problem(self, problem)
            pair.value = solution.cost

            path_line = cell_start.line
            path_column = cell_start.column
            pair.path.append(Cell(path_line, path_column))
            for action in solution.actions:
                match action.__str__():
                    case "UP":
                        path_line -= 1
                    case "DOWN":
                        path_line += 1
                    case "LEFT":
                        path_column -= 1
                    case "RIGHT":
                        path_column += 1
                pair.path.append(Cell(path_line, path_column))

    def __str__(self) -> str:
        string = "Pairs:\n"
        for p in self.pairs:
            string += f"{p}\n"
        return string


def read_state_from_txt_file(filename: str):
    with open(filename, 'r') as file:
        num_rows, num_columns = map(int, file.readline().split())
        float_puzzle = np.genfromtxt(file, delimiter=' ')
        return float_puzzle, num_rows, num_columns
