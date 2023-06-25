from ga.individual_int_vector import IntVectorIndividual
from warehouse.pair import Pair
import numpy as np
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
        self.collisions = 0

    def compute_fitness(self) -> float:
        gene = self.fitness = 0
        genome = self.fix_genome()
        all_path = {}
        goals = []
        values = []
        average = 0

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
                goals.append([steps - 1, pair.cell2.line, pair.cell2.column])
                soma += pair.value

            all_path[forklift] = forklift_path
            values.append(soma)
            # média dos tempos de cada forklift
            average += soma/self.total_forklifts

        #Calcular diferenças ao quadrado
        squared_diff = [(time - average) ** 2 for time in values]
        #Calcular variancia e desvio padrão
        variance = np.mean(squared_diff)
        std_deviation = np.sqrt(variance)
        # chama o método que encontra todas as colisões
        self.count_collisions()

        # Calcula o fitness como a soma dos tempos
        # somado com a penalização calculada
        # penalizado em 1% por cada colisão

        penalty = 0.1 * std_deviation
        self.fitness = (sum(values) + penalty) * (1.01 ** self.collisions)

        all_path = dict(sorted(all_path.items(), key=lambda item: len(item[1])))
        goals = sorted(goals, key=lambda x: x)
        all_path[self.total_forklifts] = goals
        self.all_path = all_path


        return self.fitness

    def count_collisions(self):
        collisions = step = 0
        paths_list = list(self.all_path.values())[:-1]
        while len(paths_list) > 1:
            refpath = paths_list.pop(0)
            while step < len(refpath):
                for path in paths_list:
                    if refpath[step] == path[step]:
                        collisions += 1
                step += 1
        self.collisions = collisions

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
        string += 'Collisions: ' + f'{self.collisions}' + '\n'
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.all_path = self.all_path
        new_instance.steps = self.steps
        new_instance.collisions = self.collisions
        return new_instance
