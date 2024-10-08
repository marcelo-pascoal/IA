import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()
        # defenição das barreiras físicas e uso de uma variável para diferenciar entre produto e exit
        self.walls = {constants.PRODUCT_CATCH, constants.PRODUCT, constants.SHELF}
        # posicao objectivo
        self.goal_line = 0
        self.goal_col = 0

        self.rows = rows
        self.columns = columns
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)

        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.FORKLIFT:
                    self.line_forklift = i
                    self.column_forklift = j
                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j

    # verifica se o forklift se pode mover para determinada posição
    # verifica se essa posição está nos limites da matriz E se n coresponde a uma barreira física
    def can_move_up(self) -> bool:
        return self.line_forklift != 0 \
            and self.matrix[self.line_forklift - 1][self.column_forklift] not in self.walls

    def can_move_right(self) -> bool:
        return self.column_forklift != self.columns - 1 \
            and self.matrix[self.line_forklift][self.column_forklift + 1] not in self.walls

    def can_move_down(self) -> bool:
        return self.line_forklift != self.rows - 1 \
            and self.matrix[self.line_forklift + 1][self.column_forklift] not in self.walls

    def can_move_left(self) -> bool:
        return self.column_forklift != 0 \
            and self.matrix[self.line_forklift][self.column_forklift - 1] not in self.walls

    # move o agente para a nova posição
    # atualiza a posiçao do forklift e a matriz: posiçao antiga -> EMPTY ; nova -> FORKLIFT
    def move_up(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.line_forklift -= 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT

    def move_right(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.column_forklift += 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT

    def move_down(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.line_forklift += 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT

    def move_left(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.column_forklift -= 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
