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
        new_individual = WarehouseIndividual(self, len(self.forklifts)+len(self.products))
        forklift_list = {i: [] for i in len(self.forklifts)}
        product_stack = self.products
        working = True
        while len(product_stack) != 0:
            seq = random.sample(range(len(self.forklifts)), len(self.forklifts))
            for step in seq:
                forklift = self.forklifts[step]
                closest = 0

                if len(product_stack) == 0:
                    break

                else:
                    for product in product_stack:
                        for pair in self.agent_search.pairs:
                            if pair.cell1 == forklift and pair.cell2 == product \
                                    and (pair.value < closest or not closest):
                                closest = pair.value
                                product_pick = product
                    product_stack.remove(product_pick)
                    forklift_list[step].append(product_pick)

        my_array = [3, 6, 9, 12]

        for index, element in enumerate(my_array):
            print("The element at index", index, "is", element)

        new_individual.build_genome(self, forklift_list)

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

