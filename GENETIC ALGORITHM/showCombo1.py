# -*- coding: utf-8 -*-
import time
import matplotlib.pyplot as plt
from genetic_elemental import shuffled_subjects, generate_class_time, create_timetable, plot_timetable
from function import generate_population, fitness_func, selecting_two, single_point_crossover, mutation

# Chạy hàm main
generations = 2000
population_size = 200
length = len(shuffled_subjects)

# Initialize the first population
population = generate_population(population_size, length)

# Initialize tracking variables
f = 1
top_genomes = []
previous_dad = None
previous_mom = None
society = population.copy()

# For plotting
max_fitness_over_time = []
avg_fitness_over_time = []
unique_genomes_over_time = []

start_time = time.time()
time_per_generation = []
update_frequency = 10  # Update the time estimate every 10 generations
significant_change = 1.0  # Significant change in seconds to trigger an update
last_reported_estimate = 0

# Variables to track the discovery of a genome with 24 fitness points
found_24_fitness = False
generation_found_24 = None
time_found_24 = None
total_individuals_at_24 = None

# Variable to track the total number of individuals created
total_individuals_created = population_size

# Start the generational loop
for generation in range(generations):
    gen_start_time = time.time()
    
    fitness_values = [fitness_func(ind) for ind in society]
    
    max_fitness = max(fitness_values)
    avg_fitness = sum(fitness_values) / len(fitness_values)
    unique_genomes = len(set(map(str, society)))  # Count unique genomes
    
    # Append data for plotting
    max_fitness_over_time.append(max_fitness)
    avg_fitness_over_time.append(avg_fitness)
    unique_genomes_over_time.append(unique_genomes)
    
    if generation in [1, 500, 1000, 1980]:
        print(f"\nThông tin tóm tắt cho thế hệ {generation}:")
        print(f"Max Fitness = {max_fitness}, Average Fitness = {avg_fitness}, Unique Genomes = {unique_genomes}")

    parents = selecting_two(society)
    dad, mom = parents

    # Ensure no reselection of the same parent pairs
    while (dad == previous_dad and mom == previous_mom) or (dad == previous_mom and mom == previous_dad):
        parents = selecting_two(society)
        dad, mom = parents
    previous_dad = dad
    previous_mom = mom

    cross_childs = single_point_crossover(dad, mom)
    offsprings_generation = [child for child in cross_childs if fitness_func(child) > fitness_func(dad) or fitness_func(child) > fitness_func(mom)]
    total_individuals_created += len(offsprings_generation)
    society.extend(offsprings_generation)

    mutated_child_1 = mutation(cross_childs[0])
    mutated_child_2 = mutation(cross_childs[1])
    mutated_generation = [mutated_child_1 if fitness_func(mutated_child_1) != fitness_func(cross_childs[0]) else None,
                          mutated_child_2 if fitness_func(mutated_child_2) != fitness_func(cross_childs[1]) else None]
    total_individuals_created += len(list(filter(None, mutated_generation)))
    society.extend(filter(None, mutated_generation))

    # Remove duplicate genomes
    society = list({genome.__repr__(): genome for genome in society}.values())

    # Sort new population based on fitness
    society.sort(key=fitness_func, reverse=True)
    best_genome_in_generation = max(society, key=fitness_func)
    top_genomes.append(best_genome_in_generation)

    # Check if a genome with 24 fitness points is found
    if not found_24_fitness and fitness_func(best_genome_in_generation) >= 24:
        found_24_fitness = True
        generation_found_24 = generation
        time_found_24 = time.time() - start_time
        total_individuals_at_24 = len(society)
        break  # Stop the loop

    f += 1

    # Time calculations and conditional output
    gen_end_time = time.time()
    gen_duration = gen_end_time - gen_start_time
    time_per_generation.append(gen_duration)
    average_time_per_gen = sum(time_per_generation) / len(time_per_generation)
    remaining_generations = generations - generation
    estimated_remaining_time = average_time_per_gen * remaining_generations

    if generation % update_frequency == 0 and abs(estimated_remaining_time - last_reported_estimate) >= significant_change:
        print(f"Generation {generation}: Estimated time remaining: {estimated_remaining_time:.2f} seconds")
        last_reported_estimate = estimated_remaining_time

# Calculate and output total runtime
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTotal elapsed time: {elapsed_time:.2f} seconds")

if found_24_fitness:
    print(f"\nGenome with 24 fitness points found at generation {generation_found_24}")
    print(f"Time taken to find: {time_found_24:.2f} seconds")
    print(f"Total individuals at the time of finding: {total_individuals_at_24}")
else:
    print("\nNo genome with 24 fitness points found within the given generations.")

print(f"Total number of individuals in the population when the program stopped: {len(society)}")
print(f"Total number of individuals created during the run: {total_individuals_created}")

# Calculate and print efficiency
efficiency = total_individuals_created / elapsed_time
print(f"Program efficiency: {efficiency:.2f} individuals per second")

best_genome = max(top_genomes, key=fitness_func)
best_fitness = fitness_func(best_genome)
class_time_info = generate_class_time(best_genome, shuffled_subjects)
timetable_df = create_timetable(class_time_info)
plot_timetable(timetable_df)

# Plotting results
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(max_fitness_over_time, label='Max Fitness')
plt.plot(avg_fitness_over_time, label='Average Fitness')
plt.title('Fitness Over Generations')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(unique_genomes_over_time, color='green')
plt.title('Unique Genomes Over Generations')
plt.xlabel('Generation')
plt.ylabel('Unique Genomes')
plt.tight_layout()
plt.show()

# Print the best results
print("\nBest of all generation ever found :")
print(best_genome, best_fitness)

# Print the table data
# General information about the evolution process
print("\nGeneral Information:")
print(f"Số thế hệ: {generations}")
print(f"Kích thước quần thể: {population_size}")
