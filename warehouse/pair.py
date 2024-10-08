class Pair:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2
        # valor calculado pelo A*
        self.value = 0
        # caminho desde cell1 até cell2
        self.path = []

    def hash(self):
        return str(self.cell1.line) + "_" + str(self.cell1.column) + "_" + str(
            self.cell2.line) + "_" + str(self.cell2.column)

    def __str__(self):
        return str(self.cell1.line) + "-" + str(self.cell1.column) + " / " + \
            str(self.cell2.line) + "-" + str(self.cell2.column) + ": " + str(self.value) + "\n"
