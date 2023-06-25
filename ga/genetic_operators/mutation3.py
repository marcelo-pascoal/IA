from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
import random


class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    #precorre o genoma e caso random.random() < selfprobability troca esse gene com
    # o gene adjacente (alteatoriamente esquerda ou direita)
    def mutate(self, ind: IntVectorIndividual) -> None:
        ind.genome = ind.genome
        num_genes = len(ind.genome)
        for i in range(num_genes):
            prob = random.random()
            if prob <= self.probability:
                aux = ind.genome[i]
                if random.random() < 0.5:
                    if i == 0:
                        ind.genome[i]=ind.genome[num_genes-1]
                        ind.genome[num_genes - 1]= aux
                    else:
                        ind.genome[i]=ind.genome[i-1]
                        ind.genome[i - 1] = aux
                else:
                    if i == num_genes-1:
                        ind.genome[i]=ind.genome[0]
                        ind.genome[0]= aux
                    else:
                        ind.genome[i]=ind.genome[i + 1]
                        ind.genome[i + 1] = aux

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
