from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual
from ga.genetic_algorithm import GeneticAlgorithm
import random


class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        if cut2 < cut1:
            cut1, cut2 = cut2, cut1
        mapping1 = {}
        mapping2 = {}
        for i in range(cut1, cut2 + 1):
            mapping1[ind1.genome[i]] = ind2.genome[i]
            mapping2[ind2.genome[i]] = ind1.genome[i]

        # Versao genoma dominante: quando deteta colisoes preenche com o genoma do ind com melhor fitness
        child1 = [-1] * len(ind1.genome)
        for i in range(cut1, cut2 + 1):
            child1[i] = ind1.genome[i]
        for i in range(len(ind1.genome)):
            if child1[i] == -1:
                gene = ind2.genome[i]
                if gene in mapping1:
                    if random.random() < 0.5:
                        gene = ind1.genome[i]
                    else:
                        for index, gene1 in enumerate(ind1.genome[cut1:], start=cut1):
                            if gene1 == gene:
                                break
                        child1[index] = ind2.genome[index]
                child1[i] = gene

        child2 = [-1] * len(ind1.genome)
        for i in range(cut1, cut2 + 1):
            child2[i] = ind2.genome[i]
        for i in range(len(ind1.genome)):
            if child2[i] == -1:
                gene = ind1.genome[i]
                if gene in mapping2:
                    if random.random() < 0.5:
                        gene = ind2.genome[i]
                    else:
                        for index, gene2 in enumerate(ind2.genome[cut1:], start=cut1):
                            if gene2 == gene:
                                break
                        child2[index] = ind1.genome[index]
                child2[i] = gene

        ind1.genome = child2
        ind2.genome = child1

    def __str__(self):
        return "PMX recombination (" + f'{self.probability}' + ")"
