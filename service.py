import networkx as nx
from domain import *
from random import sample
import numpy.random as npr
import tsplib95
from ui import *
import os


class Service:
    def __init__(self, repo, crossover_rate, mutation_rate, population_size, generations, selection_method):
        self.repo = repo
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = population_size
        self.generations = generations
        self.selection_method = selection_method
        self.graph = nx.Graph()
        self.genes = 10000
        self.start_location = 0
        self.fitnesses = []
        self.distance_matrix = None

    def read_input(self, path, tsp=False):
        graph = nx.Graph()

        if not tsp:
            file = open(path, "r")

            number_of_cities = int(file.readline())
            self.genes = number_of_cities

            for i in range(1, number_of_cities + 1):
                dists = file.readline()
                dists = dists.split(',')

                crt = 1
                for x in dists:
                    graph.add_edge(i, crt, weight=x, distance=x)
                    crt = crt + 1

            start_city = int(file.readline())
            self.start_location = start_city - 1
            dest_city = int(file.readline())

            self.graph = graph
            print(self.graph.nodes)
            file.close()

        else:
            problem = tsplib95.utils.load_problem(path)
            self.graph = problem.get_graph()
            self.distance_matrix = nx.to_numpy_matrix(self.graph)
            self.genes = len(self.graph)

    def print_solution(self):
        fittest = self.repo.get_fittest(self.distance_matrix)
        file = open("result.txt", "w+")
        file.write(str(self.genes) + '\n')
        file.write(" ".join(map(str, fittest.state)) + '\n')
        file.write(str(fittest.calculate_path_length(self.distance_matrix)))
        file.close()

    def create_population(self):
        for i in range(self.population):
            chromosome = Chromosome(self.genes, self.start_location)
            chromosome.calculate_fitness(self.distance_matrix)
            self.repo.add_chromosome(chromosome)

    def select_one_for_crossover(self, selection_type='roulette', tournament_size=-1):
        chromosomes = self.repo.get_chromosomes()
        chosen = None
        if selection_type is 'roulette':
            total_fitness = sum([c.fitness for c in chromosomes])
            selection_probability = [c.fitness / total_fitness for c in chromosomes]

            chosen = chromosomes[npr.choice(len(chromosomes), p=selection_probability)]
        elif selection_type is 'rank':
            chromosomes.sort(key=lambda x: x.fitness, reverse=True)
            length = len(chromosomes)
            selection_probability = [i / ((length + 1) * length / 2) for i in range(1, length + 1)]

            chosen = chromosomes[npr.choice(length, p=selection_probability)]
        elif selection_type is 'tournament':
            if tournament_size == -1:
                tournament_size = int(len(chromosomes) / 2)

            tournament = sample(chromosomes, tournament_size)
            tournament.sort(key=lambda x: x.fitness)

            chosen = tournament[-1]
        """elif selection_type is 'boltzmann':
            max_fitness = max([c.fitness for c in chromosomes])
            k = (1 + 100 * self.current_generation / self.generations)
            temp = self.initial_temp * ((1 - 0.5) ** k)
            temp = (max_fitness - min([c.fitness for c in chromosomes]))
            print(max_fitness)
            print(sum([math.exp(((max_fitness - c.fitness) / temp) * -1)/50 for c in chromosomes]))
            selection_probability = [math.exp((max_fitness - c.fitness) / temp) for c in chromosomes]

            chosen = chromosomes[npr.choice(len(chromosomes), p=selection_probability)]
        """
        return chosen

    def advance_one_generation(self, elitism=False):
        next_generation = []

        if elitism:
            fittest = self.repo.get_fittest(self.distance_matrix)
            self.repo.remove_chromosome(fittest)
            next_generation.append(fittest)

        number_to_crossover = int(self.crossover_rate * len(self.repo.get_chromosomes()) / 2)

        for i in range(number_to_crossover - 1):
            parent1 = self.select_one_for_crossover(self.selection_method)
            self.repo.remove_chromosome(parent1)
            parent2 = self.select_one_for_crossover(self.selection_method)
            self.repo.remove_chromosome(parent2)

            crossover_result = parent1.crossover_ox(parent2)

            crossover_result[0].mutate(self.mutation_rate)
            crossover_result[1].mutate(self.mutation_rate)
            crossover_result[0].calculate_fitness(self.distance_matrix)
            crossover_result[1].calculate_fitness(self.distance_matrix)

            next_generation.append(crossover_result[0])
            next_generation.append(crossover_result[1])

        for x in self.repo.get_chromosomes():
            x.mutate(self.mutation_rate)
            x.calculate_fitness(self.distance_matrix)
            next_generation.append(x)

        to_cull = int(self.population/10)

        next_generation.sort(key=lambda y: y.fitness)

        for i in range(to_cull):
            next_generation.pop(0)

        for i in range(to_cull):
            c = Chromosome(self.genes, self.start_location)
            c.calculate_fitness(self.distance_matrix)
            next_generation.append(c)

        self.repo.set_chromosomes(next_generation)

        self.fitnesses.append(1/self.repo.get_fittest(self.distance_matrix).fitness)

    def advance_one_generation2(self):
        offspring = []
        to_crossover = int(self.crossover_rate * len(self.repo.get_chromosomes()))

        for _ in range(to_crossover):
            parent1 = self.select_one_for_crossover(self.selection_method)
            parent2 = self.select_one_for_crossover(self.selection_method)

            crossover_result = parent1.crossover_ox(parent2)

            crossover_result[0].mutate_rsm(self.mutation_rate)
            crossover_result[1].mutate_rsm(self.mutation_rate)
            crossover_result[0].calculate_fitness(self.distance_matrix)
            crossover_result[1].calculate_fitness(self.distance_matrix)

            offspring.append(crossover_result[0])
            offspring.append(crossover_result[1])

        next_generation = []

        elitism_count = self.population - len(offspring) if (len(offspring) < (self.population // 2)) else self.population // 2

        for _ in range(elitism_count):
            best = self.repo.get_fittest(self.distance_matrix)
            self.repo.remove_chromosome(best)
            best.calculate_fitness(self.distance_matrix)
            next_generation.append(best)

        self.repo.set_chromosomes(offspring)

        elitism_count = len(offspring) if (len(offspring) < (self.population // 2)) else self.population // 2

        for _ in range(elitism_count):
            best = self.repo.get_fittest(self.distance_matrix)
            self.repo.remove_chromosome(best)
            best.calculate_fitness(self.distance_matrix)
            next_generation.append(best)

        self.repo.set_chromosomes(next_generation)

        self.fitnesses.append(1/self.repo.get_fittest(self.distance_matrix).fitness)

    def advance_one_generation3(self):
        offspring = []
        to_crossover = int(self.crossover_rate * len(self.repo.get_chromosomes()))

        for _ in range(to_crossover):
            parent1 = self.select_one_for_crossover(self.selection_method)
            parent2 = self.select_one_for_crossover(self.selection_method)

            crossover_result = parent1.crossover_ox(parent2)

            crossover_result[0].mutate_rsm(self.mutation_rate)
            crossover_result[1].mutate_rsm(self.mutation_rate)
            crossover_result[0].calculate_fitness(self.distance_matrix)
            crossover_result[1].calculate_fitness(self.distance_matrix)

            offspring.append(crossover_result[0])
            offspring.append(crossover_result[1])

        next_generation = []

        for x in offspring:
            self.repo.add_chromosome(x)

        for _ in range(self.population):
            best = self.repo.get_fittest(self.distance_matrix)
            self.repo.remove_chromosome(best)
            best.calculate_fitness(self.distance_matrix)
            next_generation.append(best)

        self.repo.set_chromosomes(next_generation)

        self.fitnesses.append(1/self.repo.get_fittest(self.distance_matrix).fitness)

    def run_ga(self):
        for i in range(0, self.generations):
            self.advance_one_generation3()

        return self.fitnesses