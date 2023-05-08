from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual
import random


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        # TODO
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search

    def generate_individual(self) -> "WarehouseIndividual":
        total_products = len(self.products)
        total_forklifts = len(self.forklifts)
        new_individual = WarehouseIndividual(self, total_forklifts + total_products)

        forklift_list = {}
        for i in range(total_forklifts):
            forklift_list[i] = []
        product_stack = list(range(total_products))
        product_pick = None
        while len(product_stack) != 0:
            seq = random.sample(range(total_forklifts), total_forklifts)
            for step in seq:
                if len(product_stack) == 0:
                    break
                else:
                    closest = 0
                    start_index = total_products * step
                    for product in product_stack:
                        for index, pair in enumerate(self.agent_search.pairs[start_index:], start=start_index + 1):
                            if index > start_index + total_products:
                                break
                            if pair.cell2 == self.products[product] and (pair.value < closest or not closest):
                                closest = pair.value
                                product_pick = product
                    product_stack.remove(product_pick)
                    forklift_list[step].append(product_pick)
        new_individual.build_genome(forklift_list)
        return new_individual

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string
