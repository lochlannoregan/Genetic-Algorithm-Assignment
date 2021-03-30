import random
import matplotlib.pyplot as plt


one_max_problem = False
evolving_target_string = False
deceptive_landscape_problem = True

population_size = 100

# crossover, mutation and elitism must add to 1.0
crossover_percentage = 0.8
mutation_percentage = 0.01
elitism_percentage = 0.19

number_of_individuals_for_crossover = int(population_size * crossover_percentage)
number_of_individuals_for_mutation = int(population_size * mutation_percentage)
number_of_individuals_for_elitism = int(population_size * elitism_percentage)

representation_length = 20

max_number_bits_flip_mutation = 1
k_ways = 4
generations = 100

target_string_to_evolve = "11110000111100001111"


def evolve_ga(graph_title):
    population = []
    average_generation_fitness = []

    once = False

    # Initialise population
    initialise_population(population)

    # Evolve
    for generation in range(generations):
        temp_population = []
        # Apply crossover
        crossover(temp_population, population)

        # Apply mutation
        mutation(temp_population, population)

        # Perform elitism to complete population for next generation
        elitism(temp_population, population)

        # Assemble crossover, mutation and elitism by setting population for next generation
        population = temp_population

        # Manually influencing deceptive landscape
        # once_off_representation = "00000000000000000000"
        # if not once:
        #     population[2] = {'representation': once_off_representation, 'fitness': fitness_function(
        #         once_off_representation)}
        #     population[21] = {'representation': once_off_representation, 'fitness': fitness_function(
        #         once_off_representation)}
        #     population[42] = {'representation': once_off_representation, 'fitness': fitness_function(
        #         once_off_representation)}
        #     population[41] = {'representation': once_off_representation, 'fitness': fitness_function(
        #         once_off_representation)}
        #     print("Wasup")
        #     once = True

        # Average fitness of population
        average = 0
        for individual in population:
            average += individual['fitness']
        average /= population_size
        average_generation_fitness.append(average)
        print("Generation: ", generation, format(average, ".3f"))

    # Output matplotlib graph
    graph_results(average_generation_fitness, generations, graph_title)


def initialise_population(population):
    for i in range(population_size):
        # getrandbits often gives a values less than the specified number so generating larger bit size and slicing 20
        representation = str(bin(random.getrandbits(30))[2:22])
        chromosome = {'representation': representation, 'fitness': fitness_function(representation)}
        population.append(chromosome)


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


def elitism(temp_population, population):
    for i in range(number_of_individuals_for_elitism):
        temp_population.append(k_ways_tournament_selection(population, k_ways))


def mutation(temp_population, population):
    individuals_to_mutate = []
    for i in range(number_of_individuals_for_mutation):
        individuals_to_mutate.append(k_ways_tournament_selection(population, k_ways))
    for individual in individuals_to_mutate:
        temp_population.append(mutate_bit_string(individual))


def mutate_bit_string(individual):
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
    individual['fitness'] = fitness_function(individual['representation'])
    return individual


def crossover(temp_population, population):
    crossover_parents = []
    for i in range(number_of_individuals_for_crossover):
        crossover_parents.append(k_ways_tournament_selection(population, k_ways))
    index = 1
    while index < len(crossover_parents):
        crossover_one, crossover_two = crossover_bit_strings(crossover_parents[index - 1], crossover_parents[index])
        temp_population.append(crossover_one)
        temp_population.append(crossover_two)
        index += 2


def crossover_bit_strings(individual_one, individual_two):
    crossover_one_representation = individual_one['representation'][0:10] + individual_two['representation'][10:20]
    crossover_two_representation = individual_two['representation'][0:10] + individual_one['representation'][10:20]
    crossover_one = {'representation': crossover_one_representation, 'fitness': fitness_function(
        crossover_one_representation)}
    crossover_two = {'representation': crossover_two_representation, 'fitness': fitness_function(
        crossover_two_representation)}
    return crossover_one, crossover_two


def fitness_function(individual):
    if one_max_problem:
        return individual.count('1') / representation_length
    elif evolving_target_string:
        fitness_to_return = 0
        for i, allele in enumerate(individual):
            if allele == target_string_to_evolve[i]:
                fitness_to_return += 1 / representation_length
        return fitness_to_return
    elif deceptive_landscape_problem:
        fitness_to_return = (individual.count('1') / representation_length) / 2
        if fitness_to_return == 0.0:
            fitness_to_return = 1.0
        return fitness_to_return
    else:
        print("Fitness function undefined")


def k_ways_tournament_selection(population, k_ways):
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
    evolve_ga("Deceptive Landscape")


if __name__ == '__main__':
    main()
