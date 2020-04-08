class Repository:
    def __init__(self):
        self.chromosomes = []

    def add_chromosome(self, chromosome):
        self.chromosomes.append(chromosome)

    def remove_chromosome(self, chromosome):
        self.chromosomes.remove(chromosome)

    def get_chromosomes(self):
        return self.chromosomes

    def set_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes

    def get_fittest(self, distance_matrix):
        self.chromosomes[0].calculate_fitness(distance_matrix)
        fittest = self.chromosomes[0]
        for x in self.chromosomes:
            if not x.fitness_calculated:
                x.calculate_fitness(distance_matrix)

            if x.fitness > fittest.fitness:
                fittest = x

        return fittest

    def cull_worst(self, to_cull):
        self.chromosomes.sort(key=lambda x: x.fitness)

        for i in range(to_cull):
            self.chromosomes.pop(0)

    def get_all_fitnesses(self):
        return [1/x.fitness for x in self.chromosomes]

    def get_fittest_print(self, graph):
        self.chromosomes[0].calculate_fitness(graph)
        fittest = self.chromosomes[0]
        for x in self.chromosomes:
            if not x.fitness_calculated:
                x.calculate_fitness(graph)

            print(x.fitness)

            if x.fitness > fittest.fitness:
                fittest = x

        return fittest
