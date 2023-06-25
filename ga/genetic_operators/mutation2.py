from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
import random


class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    #precorre o genoma e caso random.random() < selfprobability troca esse gene com uma posição aleatória no genoma
    def mutate(self, ind: IntVectorIndividual) -> None:
        ind.genome=ind.genome
        num_genes = len(ind.genome)
        for i in range(num_genes):
            prob = random.random()
            if prob <= self.probability:
                pos = random.randint(0, num_genes-1)
                aux = ind.genome[i]
                ind.genome[i] = ind.genome[pos]
                ind.genome[pos] = aux

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
