from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # TODO   (TER IDEIAS MELHORES/MAIS ORIGINAIS)
        # Trocar o random_cut1 para o random_cut2, o random_cut2 para o random_cut3 e o random_cut3 para o random_cut1
        num_genes = len(ind.genome)
        random_cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        random_cut2 = random_cut1
        random_cut3 = random_cut2

        while random_cut1 == random_cut2:
            random_cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

            while random_cut2 == random_cut3:
                random_cut3 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        aux = ind.genome[random_cut1]
        ind.genome[random_cut1] = ind.genome[random_cut3]
        ind.genome[random_cut3] = ind.genome[random_cut2]
        ind.genome[random_cut2] = aux

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
