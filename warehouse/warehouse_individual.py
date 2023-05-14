from ga.individual_int_vector import IntVectorIndividual


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.products = self.problem.agent_search.products
        self.forklifts = self.problem.agent_search.forklifts
        self.total_products = len(self.products)
        self.total_forklifts = len(self.forklifts)
        self.pairs = self.problem.agent_search.pairs
        self.all_path = []
        self.steps = 0

    def compute_fitness(self) -> float:
        gene = soma = 0
        genome = self.fix_genome()
        pair = None

        while gene < len(genome):
            forklift_path = []
            loop = True
            steps = 0
            path = []
            # proximo forklift
            forklift = (genome[gene] + 1) * -1
            while gene < len(genome) and loop:
                gene += 1
                # ultimo passo do forklift:   atingido o fim do genoma  ||    gene negativo (proximo forklift)
                if gene == len(genome) or genome[gene] < 0:
                    if genome[gene - 1] < 0:
                        pair = self.pairs[len(self.pairs) - (self.total_forklifts - forklift)]
                        path = pair.path
                    else:
                        pair = self.pairs[(len(self.pairs) - (self.total_products - genome[gene - 1])) - self.total_forklifts]
                        path = pair.path[1:]
                    loop = False
                # primeiro passo do forklift: gene-1 tem valor negativo (o proprio forklift)
                elif genome[gene - 1] < 0:
                    for pair in self.pairs[self.total_products * forklift:]:
                        if pair.cell2 == self.products[genome[gene]]:
                            path = pair.path
                            break
                # passo intermedio entre produtos gene -1 e gene sao positivos
                else:
                    for pair in self.pairs[(self.total_products * self.total_forklifts):]:
                        if pair.cell1 == self.products[genome[gene-1]] and pair.cell2 == self.products[genome[gene]]:
                            path = pair.path[1:]
                            break
                        elif pair.cell2 == self.products[genome[gene-1]] and pair.cell1 == self.products[genome[gene]]:
                            path = pair.path[::-1][1:]
                            break
                soma += pair.value
                forklift_path.extend(path)
                steps += len(path)

            self.all_path.append(forklift_path)
            if self.steps < steps:
                self.steps = steps

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

    def fix_genome(self) -> list:
        gene = 0
        fixed_genome = self.genome
        while fixed_genome[gene] >= 0:
            fixed_genome.append(fixed_genome.pop(0))
        return fixed_genome

    def obtain_all_path(self):
        return self.all_path, self.steps

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
