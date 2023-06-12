import numpy as np

from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination

from ga.genetic_algorithm import GeneticAlgorithm


class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        cut1 = np.random.randint(0, num_genes - 1)
        cut2 = np.random.randint(0, num_genes - 1)

        if cut2 < cut1:
            cut1, cut2 = cut2, cut1
        mapping1 = {}
        mapping2 = {}
        for i in range(cut1, cut2 + 1):
            mapping1[ind1.genome[i]] = ind2.genome[i]
            mapping2[ind2.genome[i]] = ind1.genome[i]

        child1 = [-1] * num_genes
        for i in range(cut1, cut2 + 1):
            child1[i] = ind1.genome[i]
        for i in range(num_genes):
            if child1[i] == -1:
                gene = ind2.genome[i]
                while gene in mapping1:
                    gene = mapping1[gene]
                child1[i] = gene

        child2 = [-1] * num_genes
        for i in range(cut1, cut2 + 1):
            child2[i] = ind2.genome[i]
        for i in range(num_genes):
            if child2[i] == -1:
                gene = ind1.genome[i]
                while gene in mapping2:
                    gene = mapping2[gene]
                child2[i] = gene

        """
        this code simulates gene recombination by selecting a segment of genes from each parent and exchanging them while ensuring that no duplicate genes are present in the children
        
        """
        """cut = GeneticAlgorithm.rand.randint(0, ind1.num_genes)
        for i in range(cut):
            ind1.genome[i], ind2.genome[i] = ind2.genome[i], ind1.genome[i]
            """

    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
