import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def one_max_problem():
    print("Starting one max problem")
    population_size = 100
    # crossover, mutation and elitism must add to 1.0
    crossover_percentage = 0.8
    mutation_percentage = 0.01
    elitism_percentage = 0.19

    representation_length = 20
    number_of_individuals_for_crossover = int(population_size * crossover_percentage)
    number_of_individuals_for_mutation = int(population_size * mutation_percentage)
    number_of_individuals_for_elitism = int(population_size * elitism_percentage)
    max_number_bits_flip_mutation = 1
    k_ways = 4
    generations = 100
    population = []
    average_generation_fitness = []

    # Initialise population
    for i in range(population_size):
        # getrandbits often gives a values less than the specified number so generating larger bit size and slicing 20
        representation = str(bin(random.getrandbits(30))[2:22])
        chromosome = {'representation': representation, 'fitness': fitness_function(representation,
                                                                                    representation_length)}
        population.append(chromosome)

    # Evolve
    for generation in range(generations):
        temp_population = []
        # Apply crossover
        crossover(temp_population, number_of_individuals_for_crossover, population, population_size, k_ways,
                  representation_length)

        # Apply mutation
        mutation(temp_population, number_of_individuals_for_mutation, population, population_size, k_ways, 
                 representation_length, max_number_bits_flip_mutation)

        # Perform elitism to complete population for next generation
        elitism(temp_population, number_of_individuals_for_elitism, population, population_size, k_ways)

        # Assemble crossover, mutation and elitism by setting population for next generation
        population = temp_population

        # Average fitness of population
        average = 0
        for individual in population:
            average += individual['fitness']
        average /= population_size
        average_generation_fitness.append(average)
        print("Generation: ", generation, format(average, ".3f"))

    # Output matplotlib graph
    graph_results(average_generation_fitness, generations, "One-Max GA")


def graph_results(average_generation_fitness, generations, title):
    plt.rc('axes')
    x = list(range(1, generations + 1))
    plt.plot(x, average_generation_fitness, linewidth=5)
    plt.xlim(1, generations)
    plt.ylim(0, 1)
    plt.xlabel("Generations")
    plt.ylabel("Average Population Fitness")
    plt.title(title)
    plt.show()


def elitism(temp_population, number_of_individuals_for_elitism, population, population_size, k_ways):
    for i in range(number_of_individuals_for_elitism):
        temp_population.append(k_ways_tournament_selection(population, population_size, k_ways))


def mutation(temp_population, number_of_individuals_for_mutation, population, population_size, k_ways,
             representation_length, max_number_bits_flip_mutation):
    individuals_to_mutate = []
    for i in range(number_of_individuals_for_mutation):
        individuals_to_mutate.append(k_ways_tournament_selection(population, population_size, k_ways))
    for individual in individuals_to_mutate:
        temp_population.append(mutate_bit_string(individual, representation_length, max_number_bits_flip_mutation))


def mutate_bit_string(individual, representation_length, max_number_bits_flip_mutation):
    number_of_bits_to_flip = random.randint(1, max_number_bits_flip_mutation)
    for i in range(number_of_bits_to_flip):
        position_to_flip = random.randint(0, 19)
        value = individual['representation'][position_to_flip]
        if individual['representation'][position_to_flip] == '1':
            individual['representation'] = individual['representation'][:position_to_flip] + "0" + \
                                           individual['representation'][position_to_flip + 1:]
        elif individual['representation'][position_to_flip] == '0':
            individual['representation'] = individual['representation'][:position_to_flip] + "1" + \
                                           individual['representation'][position_to_flip + 1:]
    individual['fitness'] = fitness_function(individual['representation'], representation_length)
    return individual


def crossover(temp_population, number_of_individuals_for_crossover, population, population_size, k_ways,
              representation_length):
    crossover_parents = []
    for i in range(number_of_individuals_for_crossover):
        crossover_parents.append(k_ways_tournament_selection(population, population_size, k_ways))
    index = 1
    while index < len(crossover_parents):
        crossover_one, crossover_two = crossover_bit_strings(crossover_parents[index - 1], crossover_parents[index],
                                                             representation_length)
        temp_population.append(crossover_one)
        temp_population.append(crossover_two)
        index += 2


def crossover_bit_strings(individual_one, individual_two, representation_length):
    crossover_one_representation = individual_one['representation'][0:10] + individual_two['representation'][10:20]
    crossover_two_representation = individual_two['representation'][0:10] + individual_one['representation'][10:20]
    crossover_one = {'representation': crossover_one_representation, 'fitness': fitness_function(
        crossover_one_representation, representation_length)}
    crossover_two = {'representation': crossover_two_representation, 'fitness': fitness_function(
        crossover_two_representation, representation_length)}
    return crossover_one, crossover_two


def fitness_function(individual, representation_length):
    return individual.count('1') / representation_length


def k_ways_tournament_selection(population, population_size, k_ways):
    k_random_indices = [random.randint(0, population_size - 1) for k in range(k_ways)]
    max_value = 0
    location = 0
    for k in k_random_indices:
        individual_checking = population[k]
        if individual_checking['fitness'] > max_value:
            max_value = individual_checking['fitness']
            location = k
    parent_selected = population[location]
    return parent_selected


def main():
    print("Starting program")
    one_max_problem()


if __name__ == '__main__':
    main()
