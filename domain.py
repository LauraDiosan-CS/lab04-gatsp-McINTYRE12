import numpy as np
from random import randint, random, shuffle


class Chromosome:
    def __init__(self, genes, start):
        self.state = list(np.random.default_rng().permutation(list(range(1, genes + 1))))
        shuffle(self.state)
        self.fitness = 0
        self.start = start
        self.fitness_calculated = False
        self.genes = genes

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def calculate_fitness(self, distance_matrix):
        distance_sum = self.calculate_path_length(distance_matrix)

        self.fitness_calculated = True
        self.fitness = 1 / distance_sum

        return self.fitness

    def calculate_path_length(self, distance_matrix):
        distance_sum = 0

        for i in range(self.genes - 1):
            distance_sum += distance_matrix[self.state[i] - 1, self.state[i + 1] - 1]

        distance_sum += distance_matrix[self.state[self.genes - 1] - 1, self.state[0] - 1]

        return distance_sum

    def test_path(self, distance_matrix):
        self.state = [21, 0, 48, 31, 17, 30, 20, 41, 1, 6, 16, 2, 44, 18, 40, 7, 8, 9, 32, 50, 10, 51, 13, 12, 26, 46, 25, 27, 11, 42, 14, 5, 3, 24, 45, 36, 47, 23, 4, 37, 39, 38, 35, 34, 33, 43, 15, 49, 19, 28, 29, 22]

        distance_sum = 0

        for i in range(self.genes - 1):
            distance_sum += distance_matrix[self.state[i], self.state[i + 1]]

        distance_sum += distance_matrix[self.state[self.genes - 1], self.state[0]]

        print(distance_sum)

    def crossover_cx(self, parent2):
        parent1 = self.get_state()
        parent2 = parent2.get_state()

        cycles = [-1] * len(parent1)
        cycle_no = 1
        cyclestart = (i for i, v in enumerate(cycles) if v < 0)

        for pos in cyclestart:

            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                pos = parent1.index(parent2[pos])

            cycle_no += 1

        child1 = [parent1[i] if n % 2 else parent2[i] for i, n in enumerate(cycles)]
        child2 = [parent2[i] if n % 2 else parent1[i] for i, n in enumerate(cycles)]

        offspring1 = Chromosome(self.genes, self.start)
        offspring1.set_state(child1)

        offspring2 = Chromosome(self.genes, self.start)
        offspring2.set_state(child2)

        return [offspring1, offspring2]

    def crossover(self, mate):
        mate_state = mate.get_state()
        own_state = self.get_state()

        gene1 = int(random() * len(own_state))
        gene2 = int(random() * len(own_state))

        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)

        offspring_state_1 = []

        for i in range(start_gene, end_gene):
            offspring_state_1.append(own_state[i])

        offspring_state_2 = [item for item in mate_state if item not in offspring_state_1]

        offspring1 = Chromosome(self.genes, self.start)
        offspring1.set_state(offspring_state_1 + offspring_state_2)

        offspring_state_1 = []

        for i in range(start_gene, end_gene):
            offspring_state_1.append(mate_state[i])

        offspring_state_2 = [item for item in own_state if item not in offspring_state_1]

        offspring2 = Chromosome(self.genes, self.start)
        offspring2.set_state(offspring_state_1 + offspring_state_2)

        return [offspring1, offspring2]

    def crossover_ox(self, parent2):
        p1 = self.state
        p2 = parent2.state

        c1 = [None] * len(p1)
        c2 = [None] * len(p1)

        gene1 = int(random() * len(p1))
        gene2 = int(random() * len(p1))

        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)

        for i in range(start_gene, end_gene):
            c1[i] = p1[i]

        for x in p2:
            if x not in c1:
                crt = 0
                while c1[crt] is not None:
                    crt += 1
                c1[crt] = x

        for i in range(start_gene, end_gene):
            c2[i] = p2[i]

        for x in p1:
            if x not in c2:
                crt = 0
                while c2[crt] is not None:
                    crt += 1
                c2[crt] = x

        offspring1 = Chromosome(self.genes, self.start)
        offspring1.set_state(c1)

        offspring2 = Chromosome(self.genes, self.start)
        offspring2.set_state(c2)

        return [offspring1, offspring2]

    def mutate(self, probability):
        mutate_draw = random()

        if mutate_draw < probability:
            gene1 = randint(0, self.genes - 1)
            gene2 = randint(0, self.genes - 1)

            self.state[gene1], self.state[gene2] = self.state[gene2], self.state[gene1]

    def mutate_rsm(self, probability):
        mutate_draw = random()

        if mutate_draw < probability:
            gene1 = int(random() * self.genes)
            gene2 = int(random() * self.genes)

            start_gene = min(gene1, gene2)
            end_gene = max(gene1, gene2)

            sublist = self.state[start_gene:end_gene]
            sublist.reverse()
            self.state[start_gene:end_gene] = sublist
