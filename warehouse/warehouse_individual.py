from ga.individual_int_vector import IntVectorIndividual
import constants


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        # TODO

    def compute_fitness(self) -> float:
        products = self.problem.agent_search.products
        forklifts = self.problem.agent_search.forklifts
        total_products = len(products)
        total_forklifts = len(forklifts)

        loopback = False
        gene = 0
        soma = 0

        products[self.genome[gene]]
        while self.genome[gene] >= 0:
            gene += 1
            loopback = True
        while gene < len(self.genome) - 1:
            forklift = (self.genome[gene] + 1) * -1
            gene += 1
            while self.genome[gene] >= 0:
                for pair in self.problem.agent_search.pairs[total_products * forklift:]:
                    if pair.cell2 == products[self.genome[gene]]:
                        soma += pair.value
                        break
                gene += 1
                if gene + 1 > len(self.genome):
                    break
                if self.genome[gene] < 0:
                    exit_pair = self.problem.agent_search.pairs[len(self.problem.agent_search.pairs) - (total_forklifts - forklift)]
                    soma += exit_pair.value
                    break
        if loopback:
            while self.genome[gene] >= 0:
                for pair in self.problem.agent_search.pairs[total_products * forklift:]:
                    if pair.cell2 == products[self.genome[gene]]:
                        soma += pair.value
                        break
                gene += 1
                if self.genome[gene] < 0:
                    exit_pair = self.problem.agent_search.pairs[len(self.problem.agent_search.pairs) - (total_forklifts - forklift)]
                    soma += exit_pair.value
                    break

        self.fitness = soma
        return soma

    def build_genome(self, forklift_list: dict):
        gene = 0
        for key, lista in forklift_list.items():
            self.genome[gene] = (key * -1) - 1
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
