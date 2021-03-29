import random


def one_max_problem():
    print("Starting one max problem")
    population_size = 100
    crossover_percentage = 0.8
    mutation_percentage = 0.01
    representation_length = 20
    number_of_individuals_for_crossover = int(population_size * crossover_percentage)
    number_of_parents_for_mutation = int(population_size * mutation_percentage)
    k_ways = 4
    generations = 100
    population = []
    # Initialise population
    for i in range(population_size):
        # getrandbits often gives a values less than the specified number so generating larger bit size and slicing 20
        representation = str(bin(random.getrandbits(30))[2:22])
        chromosome = {'representation': representation, 'fitness': fitness_function(representation,
                                                                                    representation_length)}
        population.append(chromosome)

    # for chromosome in population:
    #     print(chromosome['fitness'])
    # Evolve population
    for generation in range(generations):
        temp_population = []
        # Apply crossover
        crossover(temp_population, number_of_individuals_for_crossover, population, population_size, k_ways,
                  representation_length)
        print("Hello")
        # Apply mutation

        # Merge into population

        # asses fitness
        # for chromosome in population:
        #     print(fitness_function(chromosome['representation']), chromosome['fitness'])


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
