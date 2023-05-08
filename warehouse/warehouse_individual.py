from ga.individual_int_vector import IntVectorIndividual
import constants


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        # TODO

    def compute_fitness(self) -> float:
        # somar as distancias entre os produtos ate encontrar um forklift.
        # Nesse caso distancia ate à saida. Continuar a soma
        self.fitness = 0
        for i in range(self.num_genes):
            pass
        return 0

    def build_genome(self, forklift_list: dict):
        gene = 0

        for key, lista in forklift_list.items():
            self.genome[gene] = key * -1
            gene += 1

            for product in lista:
                self.genome[gene] = product
                gene += 1

    def obtain_all_path(self):
        # TODO
        pass

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        # TODO
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # TODO
        return new_instance
