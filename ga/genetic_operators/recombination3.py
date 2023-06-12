from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual
from ga.genetic_algorithm import GeneticAlgorithm


class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        child1 = [-1] * num_genes
        child2 = [-1] * num_genes

        # Randomly select two cut points
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 2)
        cut2 = GeneticAlgorithm.rand.randint(cut1 + 1, num_genes - 1)

        # Create the mask for genes to be swapped
        mask = [False] * num_genes
        mask[cut1:cut2+1] = [True] * (cut2 - cut1 + 1)

        # Perform gene swapping
        for i in range(num_genes):
            child1[i] = [ind1.genome[i] if mask[i] else ind2.genome[i] for i in range(num_genes)]

        for i in range(cut1, cut2 + 1):
            child2[i] = [ind2.genome[i] if mask[i] else ind1.genome[i] for i in range(num_genes)]

        """
        cut1 = GeneticAlgorithm.rand.randint(0, ind1.num_genes)
        cut2 = GeneticAlgorithm.rand.randint(0, ind2.num_genes)
        
        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        for i in range(cut1, cut2):
            ind1.genome[i], ind2.genome[i] = ind2.genome[i], ind1.genome[i]
        """

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"