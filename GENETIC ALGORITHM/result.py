# -*- coding: utf-8 -*-
import sys
from genetic_elemental import shuffled_subjects, generate_class_time, create_timetable, plot_timetable
from function import generate_population, fitness_func, selecting_two, single_point_crossover, mutation
def run_genetic_algorithm():
    generations = 1000
    population_size = 200
    length = len(shuffled_subjects)
    population = generate_population(population_size, length)
    f = 1
    top_genomes = []
    previous_dad = None
    previous_mom = None
    society = population.copy()
    
    for generation in range(generations):  
        # sys.stderr.write("\nat generation " + str(f) + ":\n")
        fitness_bucket = []
        
        for i in range(len(society)):
            fitness_bucket.append(fitness_func(society[i]))
        # sys.stderr.write(str(fitness_bucket) + "---số lượng cá thể cá thể ở thế hệ " + str(f) + " là " + str(len(society)) + "\n")
        
        parents = selecting_two(society, fitness_func)
        dad = parents[0]
        mom = parents[1]
        
        while (dad == previous_dad and mom == previous_mom) or (dad == previous_mom and mom == previous_dad):
            parents = selecting_two(society, fitness_func)
            dad = parents[0]
            mom = parents[1]

        # sys.stderr.write("\nDad: " + str(dad) + " " + str(fitness_func(dad)) + "\n")
        # sys.stderr.write("\nMom: " + str(mom) + " " + str(fitness_func(mom)) + "\n")
        previous_dad = dad
        previous_mom = mom

        cross_childs = single_point_crossover(dad, mom)
        offsrpings_generation = []
        
        for i in range(len(cross_childs)):
            # sys.stderr.write("\nchild " + str(i+1) + ": " + str(cross_childs[i]) + " " + str(fitness_func(cross_childs[i])) + "\n")
            if fitness_func(cross_childs[i]) > fitness_func(parents[i]):
                offsrpings_generation.append(cross_childs[i])
                
        society.extend(offsrpings_generation)
        
        mutated_child_1 = mutation(cross_childs[0])
        mutated_child_2 = mutation(cross_childs[1])
        # sys.stderr.write("\nmutated kid1: " + str(mutated_child_1) + " " + str(fitness_func(mutated_child_1)) + "\n")
        # sys.stderr.write("\nmutated kid2: " + str(mutated_child_2) + " " + str(fitness_func(mutated_child_2)) + "\n")
        
        mutated_generation = []
        if fitness_func(mutated_child_1) != fitness_func(cross_childs[0]):
            mutated_generation.append(mutated_child_1)
        if fitness_func(mutated_child_2) != fitness_func(cross_childs[1]):
            mutated_generation.append(mutated_child_2)
            
        society.extend(mutated_generation)
        
        # Loại bỏ các genome trùng lặp
        unique_society = []
        for genome in society:
            if genome not in unique_society:
                unique_society.append(genome)
        society = unique_society
        
        society.sort(key=lambda genome: fitness_func(genome), reverse=True)
        top_genomes.append(society[0])
        
        f += 1
        
    best_genome = max(top_genomes, key=lambda genome: fitness_func(genome))
    
    class_time_info = generate_class_time(best_genome, shuffled_subjects)
    timetable_df = create_timetable(class_time_info)
    
    return timetable_df.to_json()

if __name__ == "__main__":
    json_output = run_genetic_algorithm()
    print(json_output)  # This line is necessary to see the result.
