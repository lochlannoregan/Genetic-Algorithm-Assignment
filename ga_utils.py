import random
import matplotlib.pyplot as plt


def initialise_population(population, population_size, fitness_function, representation_length):
    for i in range(population_size):
        representation = ""
        for j in range(representation_length):
            representation += str(random.randint(0, 1))
        chromosome = {'representation': representation, 'fitness': fitness_function(representation)}
        population.append(chromosome)


def graph_results(generation_fitness_list, generations, title, y_label, y_limit):
    plt.rc('axes')
    x = list(range(1, generations + 1))
    plt.plot(x, generation_fitness_list, linewidth=5)
    plt.xlim(1, generations)
    plt.ylim(0, y_limit)
    plt.xlabel("Generations")
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def elitism(temp_population, population, number_of_individuals_for_elitism, k_ways, population_size):
    for i in range(number_of_individuals_for_elitism):
        temp_population.append(k_ways_tournament_selection(population, k_ways, population_size))


def mutation(temp_population, population, number_of_individuals_for_mutation, k_ways, maximum_mutation_bits_to_flip,
             population_size, fitness_function, representation_length):
    individuals_to_mutate = []
    for i in range(number_of_individuals_for_mutation):
        individuals_to_mutate.append(k_ways_tournament_selection(population, k_ways, population_size))
    for individual in individuals_to_mutate:
        temp_population.append(mutate_bit_string(individual, maximum_mutation_bits_to_flip, fitness_function,
                                                 representation_length))


def mutate_bit_string(individual, maximum_mutation_bits_to_flip, fitness_function, representation_length):
    number_of_bits_to_flip = random.randint(1, maximum_mutation_bits_to_flip)
    for i in range(number_of_bits_to_flip):
        position_to_flip = random.randint(0, representation_length - 1)
        value = individual['representation'][position_to_flip]
        if individual['representation'][position_to_flip] == '1':
            individual['representation'] = individual['representation'][:position_to_flip] + "0" + \
                                           individual['representation'][position_to_flip + 1:]
        elif individual['representation'][position_to_flip] == '0':
            individual['representation'] = individual['representation'][:position_to_flip] + "1" + \
                                           individual['representation'][position_to_flip + 1:]
    individual['fitness'] = fitness_function(individual['representation'])
    return individual


def crossover(temp_population, population, number_of_individuals_for_crossover, k_ways, population_size,
              fitness_function):
    crossover_parents = []
    for i in range(number_of_individuals_for_crossover):
        crossover_parents.append(k_ways_tournament_selection(population, k_ways, population_size))
    index = 1
    while index < len(crossover_parents):
        crossover_one, crossover_two = crossover_bit_strings(crossover_parents[index - 1], crossover_parents[index],
                                                             fitness_function)
        temp_population.append(crossover_one)
        temp_population.append(crossover_two)
        index += 2


def crossover_bit_strings(individual_one, individual_two, fitness_function):
    crossover_one_representation = individual_one['representation'][0:10] + individual_two['representation'][10:20]
    crossover_two_representation = individual_two['representation'][0:10] + individual_one['representation'][10:20]
    crossover_one = {'representation': crossover_one_representation, 'fitness': fitness_function(
        crossover_one_representation)}
    crossover_two = {'representation': crossover_two_representation, 'fitness': fitness_function(
        crossover_two_representation)}
    return crossover_one, crossover_two


def k_ways_tournament_selection(population, k_ways, population_size):
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
