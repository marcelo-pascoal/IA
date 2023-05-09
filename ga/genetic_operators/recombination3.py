from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual

from WarehouseProject_TODO.ga.genetic_algorithm import GeneticAlgorithm


class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        cut1 = GeneticAlgorithm.rand.randint(0, ind1.num_genes)
        cut2 = GeneticAlgorithm.rand.randint(0, ind1.num_genes)
        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        for i in range(cut1, cut2):
            ind1.genome[i], ind2.genome[i] = ind2.genome[i], ind1.genome[i]

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"