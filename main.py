from service import Service
from repository import Repository
from ui import *


def main():
    repo = Repository()
    service = Service(repo, 0.7, 0.1, 50, 250, 'rank')
    service.read_input("Input/berlin52", True)
    service.create_population()
    fitness = service.run_ga()

    service.print_solution()

    #draw_graph(service.graph)

    print(repo.get_fittest(service.distance_matrix))
    plot_fitness(fitness)


if __name__ == '__main__':
    main()
