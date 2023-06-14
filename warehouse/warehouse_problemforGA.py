from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual
import random


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search

    # geraçao de individuo informado (product pick)
    def generate_informed_individual(self) -> "WarehouseIndividual":
        total_products = len(self.products)
        total_forklifts = len(self.forklifts)
        # criação de indivíduo com tamanho do genoma = numero de forklifts + numero de produtos
        new_individual = WarehouseIndividual(self, total_forklifts + total_products)

        # dicionario para criação de "pick lists" por forklift
        forklift_list = {}
        for i in range(total_forklifts):
            # cria uma entrada no dicionario para cada forklift com uma lista vazia
            forklift_list[i] = []
        # criação de uma lista numerica relativa a todos os produtos a distribuir
        product_stack = list(range(total_products))
        # proximo produto
        product_pick = None

        # enquanto existirem produtos a distribuir
        while len(product_stack) != 0:
            # cria uma lista de ordem aleatoria dos forklifts
            seq = random.sample(range(total_forklifts), total_forklifts)

            #para cada forklift (sequencial aleatorio)
            for step in seq:
                #se já não existirem produtos a distribuir
                if len(product_stack) == 0:
                    break
                else:
                    # variavel para encontrar o produto mais proximo do forklift
                    # (!!! PERIGO... N FOI TIDO EM CONTA FORKLIFTS SEM PRODUTOS.. TEM DE SER CORRIGIDO !!!)
                    closest = 0
                    # variavel de index para saltar para os pares do forklift (step) a avaliar
                    start_index = total_products * step
                    for product in product_stack:
                        for index, pair in enumerate(self.agent_search.pairs[start_index:], start=start_index + 1):
                            # caso chegue ao fim da lista o produto já foi obrigatoriamente encontrado
                            if index > start_index + total_products:
                                break
                            # se encontrar um produto mais proximo guarda o seu custo e a referencia desse produto
                            if pair.cell2 == self.products[product] and (pair.value < closest or not closest):
                                closest = pair.value
                                product_pick = product
                    #remove o produto escolhido da lista
                    product_stack.remove(product_pick)
                    #adiciona o produto escolhido ao dicionario de "pick lists"
                    forklift_list[step].append(product_pick)

        # constroi o genoma do individuo

        new_individual.build_informed_genome(forklift_list)
        return new_individual

    # geração aleatoria de individuo
    def generate_individual(self) -> "WarehouseIndividual":
        size = len(self.products) + len(self.forklifts)
        new_individual = WarehouseIndividual(self, size)
        new_individual.build_genome(size)
        return new_individual

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string
