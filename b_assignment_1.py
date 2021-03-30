from ga_utils import initialise_population, graph_results, crossover, mutation, elitism

knapsack_item_values = [78, 35, 89, 36, 94, 75, 74, 79, 80, 16]
knapsack_item_weights = [18, 9, 23, 20, 59, 61, 70, 75, 76, 30]
# Problem 1 - 103
# Problem 2 - 156
knapsack_weight_limit = 156

population_size = 1000
generations = 500
representation_length = len(knapsack_item_values)
k_ways = 5

# crossover, mutation and elitism must add to 1.0
crossover_percentage = 0.8
mutation_percentage = 0.01
maximum_mutation_bits_to_flip = 5
elitism_percentage = 0.19
number_of_individuals_for_crossover = int(population_size * crossover_percentage)
number_of_individuals_for_mutation = int(population_size * mutation_percentage)
number_of_individuals_for_elitism = int(population_size * elitism_percentage)


def knapsack_problem():
    population = []
    average_generation_fitness = []
    best_generation_fitness = []

    initialise_population(population, population_size, fitness_function, representation_length)

    for generation in range(generations):
        temp_population = []
        # Apply crossover
        crossover(temp_population, population, number_of_individuals_for_crossover, k_ways, population_size,
                  fitness_function)
        # Apply mutation
        mutation(temp_population, population, number_of_individuals_for_mutation, k_ways, maximum_mutation_bits_to_flip,
                 population_size, fitness_function, representation_length)
        # Perform elitism to complete population for next generation
        elitism(temp_population, population, number_of_individuals_for_elitism, k_ways, population_size)
        # Assemble crossover, mutation and elitism by setting population for next generation
        population = temp_population
        # Average fitness of population
        average = 0
        best = 0
        for individual in population:
            average += individual['fitness']
            if individual['fitness'] > best:
                best = individual['fitness']
        average /= population_size
        average_generation_fitness.append(average)
        best_generation_fitness.append(best)
        print("Generation: ", generation, format(average, ".3f"))
    # Output matplotlib graph
    graph_results(average_generation_fitness, generations, "Knapsack Problem 2", "Average Population Fitness",
                  max(average_generation_fitness))
    graph_results(best_generation_fitness, generations, "Knapsack Problem 2", "Best Population Fitness",
                  max(best_generation_fitness))
    max_best_fitness = 0
    index = 0
    for i, individual in enumerate(population):
        if individual['fitness'] > max_best_fitness:
            max_best_fitness = individual['fitness']
            index = i
    print("Maximum fitness ", max_best_fitness, "with solution", population[index]['representation'])


def fitness_function(individual):
    weight_sum = 0
    value_sum = 0
    for i in range(representation_length):
        if individual[i] == '1':
            weight_sum += knapsack_item_weights[i]
            value_sum += knapsack_item_values[i]
    if weight_sum > knapsack_weight_limit:
        value_sum = 0
    return value_sum


def main():
    knapsack_problem()


if __name__ == '__main__':
    main()
