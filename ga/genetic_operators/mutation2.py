from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation


class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        # Troca o ultimo gene com o primeiro (vice versa)
        aux = ind.genome[0]
        ind.genome[0] = ind.genome[num_genes-1]
        ind.genome[num_genes-1] = aux

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
