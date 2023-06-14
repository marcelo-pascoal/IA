from ga.individual_int_vector import IntVectorIndividual
from warehouse.pair import Pair
from typing import Tuple
import random


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.products = self.problem.agent_search.products
        self.forklifts = self.problem.agent_search.forklifts
        self.total_products = len(self.products)
        self.total_forklifts = len(self.forklifts)
        self.pairs = self.problem.agent_search.pairs
        self.all_path = {}
        self.steps = 0

    def compute_fitness(self) -> float:
        gene = self.fitness = 0
        genome = self.fix_genome()
        all_path = {}
        goals = self.total_forklifts
        all_path[goals] = []

        while gene < len(genome):
            steps = 0
            forklift_path = []
            path = []
            soma = 0
            loop = True
            # próximo forklift
            forklift = genome[gene] - self.total_products
            while gene < len(genome) and loop:
                gene += 1
                # último passo do forklift: atingido o fim do genoma || gene maior q total_products (proximo forklift)
                if gene == len(genome) or genome[gene] >= self.total_products:
                    if genome[gene - 1] >= self.total_products:
                        pair = self.pairs[len(self.pairs) - (self.total_forklifts - forklift)]
                        path = pair.path
                    else:
                        pair = self.pairs[(len(self.pairs) - (self.total_products - genome[gene-1])) - self.total_forklifts]
                        path = pair.path[1:]
                    loop = False
                # primeiro passo do forklift: gene-1 tem valor maior q total_products (o próprio forklift)
                elif genome[gene - 1] >= self.total_products:
                    for pair in self.pairs[self.total_products * forklift:]:
                        if pair.cell2 == self.products[genome[gene]]:
                            path = pair.path
                            break
                # passo intermédio entre produtos
                else:
                    for pair in self.pairs[(self.total_products * self.total_forklifts):]:
                        if pair.cell1 == self.products[genome[gene-1]] and pair.cell2 == self.products[genome[gene]]:
                            path = pair.path[1:]
                            break
                        elif pair.cell2 == self.products[genome[gene-1]] and pair.cell1 == self.products[
                            genome[gene]]:
                            path = pair.path[::-1][1:]
                            pair = Pair(pair.cell2, pair.cell1)
                            break
                forklift_path.extend(path)
                steps += len(path)
                all_path[goals].append([steps - 1, pair.cell2.line, pair.cell2.column])
                soma += pair.value

            all_path[forklift] = forklift_path

            if self.steps < steps:
                self.steps = steps
            if self.fitness < soma:
                self.fitness = soma

        all_path[goals] = sorted(all_path[goals], key=lambda x: x)
        self.all_path = {k: all_path[k] for k in sorted(all_path)}
        return self.fitness

    # metodo que constroi o genoma informado do indivíduo
    def build_informed_genome(self, forklift_list: dict):
        gene = 0
        for key, lista in forklift_list.items():
            self.genome[gene] = key + self.total_products
            gene += 1

            for product in lista:
                self.genome[gene] = product
                gene += 1

    # metodo que constroi o genoma aleatorio do indivíduo
    def build_genome(self, size: int):
        genome = random.sample(range(size), size)
        self.genome = genome

    # corrige o genoma para calculo de fitness ou caminho para simulaçao
    def fix_genome(self) -> list:
        fixed_genome = list(self.genome)
        while fixed_genome[0] < self.total_products:
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
