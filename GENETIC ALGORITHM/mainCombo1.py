# -*- coding: utf-8 -*-
from genetic_elemental import shuffled_subjects,generate_class_time,create_timetable,plot_timetable
from function import generate_population,fitness_func,selecting_two,single_point_crossover,mutation
generations = 20
population_size = 10
length = len(shuffled_subjects)
# GENETIC BEGIN HERE
population = generate_population(population_size,length)
# tạo biến f để theo dõi và đánh dấu các thế hệ
f = 1
# tạo mảng để chứa các cá thể siêu việt ở mỗi thế hệ
top_genomes = []
previous_dad = None
previous_mom = None
society = population.copy()
# bắt đầu vòng lặp
for generation in range(generations):  
    print("\nat generation ",f,":")
    fitness_bucket = []
    for i in range(len(society)):
        fitness_bucket.append(fitness_func(society[i]))
    print(fitness_bucket,"---số lượng cá thể cá thể ở thế hệ",f, "là", len(society))
    # 1
    parents = selecting_two(society)
    dad = parents[0]
    mom = parents[1]
    # Kiểm tra xem cặp đã được chọn trước đó chưa, nếu đã chọn rồi thì không được chọn lại
    while (dad == previous_dad and mom == previous_mom) or (dad == previous_mom and mom == previous_dad):
        dad, mom = selecting_two(society)
    print("\nDad:",parents[0],fitness_func(parents[0]))
    print("\nMom:",parents[1],fitness_func(parents[1]))
    previous_dad = dad
    previous_mom = mom

    cross_childs = single_point_crossover(parents[0],parents[1])
    offsrpings_generation = []
    for i in range(len(cross_childs)):
        print("\nchild",i+1,":",cross_childs[i],fitness_func(cross_childs[i]))
    if fitness_func(cross_childs[0]) > fitness_func(parents[0]):
        offsrpings_generation.append(cross_childs[0])
    if fitness_func(cross_childs[1]) > fitness_func(parents[1]):
        offsrpings_generation.append(cross_childs[1])
    society.extend(offsrpings_generation)
    # 3
    mutated_child_1 = mutation(cross_childs[0])
    mutated_child_2 = mutation(cross_childs[1])
    print("\nmutated kid1:",mutated_child_1,fitness_func(mutated_child_1))
    print("\nmutated kid2:",mutated_child_2,fitness_func(mutated_child_2))
    mutated_generation = []
    if fitness_func(mutated_child_1) > fitness_func(cross_childs[0]):
        mutated_generation.append(mutated_child_1)
    if fitness_func(mutated_child_2) > fitness_func(cross_childs[1]):
        mutated_generation.append(mutated_child_2)
    society.extend(mutated_generation)
    unique_society = []
    # lọc genome trùng nhau
    for genome in society:
        if genome not in unique_society:
            unique_society.append(genome)
    society = unique_society    
    #  Sắp xếp lại quần thể mới
    society.sort(key=lambda genome: fitness_func(genome), reverse=True)
    best_genome_in_generation = max(society, key=lambda genome: fitness_func(genome))
    top_genomes.append(best_genome_in_generation)
    best_genome = max(top_genomes, key=lambda genome: fitness_func(genome))
    best_fitness = fitness_func(best_genome)
    f += 1
    # create loop
population = society
print("\nBest genomes of each generation:")
for i, genome in enumerate(top_genomes, start=1):
    print("Generation", i, ":", genome,fitness_func(genome))
print("\nBest of all generation ever found :")
print(best_genome,best_fitness)
print(fitness_func(best_genome))
class_time_info = generate_class_time(best_genome, shuffled_subjects)
timetable_df = create_timetable(class_time_info)
plot_timetable(timetable_df)