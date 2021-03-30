from ga_utils import initialise_population, crossover, mutation, elitism, graph_results

one_max_problem = False
evolving_target_string = False
target_string_to_evolve = "11110000111100001111"
deceptive_landscape_problem = True

population_size = 100
generations = 100
representation_length = 20
k_ways = 4

# crossover, mutation and elitism must add to 1.0
crossover_percentage = 0.8
mutation_percentage = 0.01
maximum_mutation_bits_to_flip = 1
elitism_percentage = 0.19
number_of_individuals_for_crossover = int(population_size * crossover_percentage)
number_of_individuals_for_mutation = int(population_size * mutation_percentage)
number_of_individuals_for_elitism = int(population_size * elitism_percentage)


def evolve_ga(graph_title):
    population = []
    average_generation_fitness = []
    # Initialise population
    initialise_population(population, population_size, fitness_function)
    # Evolve
    for generation in range(generations):
        temp_population = []
        # Apply crossover
        crossover(temp_population, population, number_of_individuals_for_crossover, k_ways, population_size,
                  fitness_function)
        # Apply mutation
        mutation(temp_population, population, number_of_individuals_for_mutation, k_ways, maximum_mutation_bits_to_flip,
                 population_size, fitness_function)
        # Perform elitism to complete population for next generation
        elitism(temp_population, population, number_of_individuals_for_elitism, k_ways, population_size)
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
    graph_results(average_generation_fitness, generations, graph_title)


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


def main():
    evolve_ga("Deceptive Landscape")


if __name__ == '__main__':
    main()
