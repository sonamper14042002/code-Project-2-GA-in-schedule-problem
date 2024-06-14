from typing import List, Callable, Tuple
import random
from genetic_elemental import shuffled_subjects
from def_fitness_function import fitness

# Define data types
Genome = List[int]
Population = List[Genome]
fitness_value = Callable[[Genome], int]
weight_limit = 1
fitness_func = lambda genome: fitness(genome, shuffled_subjects, weight_limit)

def generate_genome(length: int) -> Genome:
    # Function to create a genome consisting of random 0s or 1s
    return [random.randint(0, 1) for _ in range(length)]

def generate_population(size: int, length: int) -> Population:
    # Function to generate a population of unique genomes
    population = set()
    # Ensure that there is at least a minimum size to accommodate both special genomes
    if size < 2:
        raise ValueError("Population size must be at least 2 to include both all-0s and all-1s genomes")
    # Add genomes that are all 0s and all 1s
    # all_ones = tuple([1] * length)
    # population.add(all_ones)
    # Continue adding random unique genomes until the population is of the desired size
    while len(population) < size:
        new_genome = tuple(generate_genome(length))
        population.add(new_genome)
    return [list(genome) for genome in population]  # Convert tuples back to lists if needed

def selecting_two(population: List[Genome]) -> Tuple[Genome, Genome]:
    return tuple(random.sample(population, 2))

def selecting_top_two(population: List[Genome]) -> Tuple[Genome, Genome]:
    return tuple(population[:2])

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    length = len(a)
    point1 = random.randint(1, length - 1) 
    child_a = a[:point1] + b[point1:]
    child_b = b[:point1] + a[point1:]
    return (child_a, child_b)


def multi_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    length = len(a)
    point1 = random.randint(1, length - 3)  # Đảm bảo point1 không quá gần cuối cùng
    point2 = random.randint(point1 + 1, length - 2)  # Đảm bảo khoảng cách giữa point1 và point2 ít nhất là 1
    point3 = random.randint(point2 + 1, length - 1)  # Đảm bảo khoảng cách giữa point2 và point3 ít nhất là 1
    child_a = a[:point1] + b[point1:point2] + a[point2:point3] + b[point3:]
    child_b = b[:point1] + a[point1:point2] + b[point2:point3] + a[point3:]
    return (child_a, child_b)


def mutation(genome: Genome, num: int = 1, probability: float = 0.7) -> Genome:
    # Function to mutate a genome with given probability and number of mutations
    mutated_genome = genome[:]  # Create a copy of the original genome
    for _ in range(num):
        index = random.randrange(len(mutated_genome))  # Choose a random index to mutate
        if random.random() <= probability:  # Only mutate with a certain probability
            mutated_genome[index] = 1 - mutated_genome[index]  # Flip the bit (0 to 1 or 1 to 0)
    return mutated_genome

def multi_point_mutation(genome: Genome, probability: float = 0.7) -> Genome:
    num = random.randint(0, len(genome))  # Chọn số lượng điểm đột biến ngẫu nhiên từ 0 đến độ dài của genome
    mutated_genome = genome[:]  # Tạo một bản sao của genome gốc
    for _ in range(num):
        index = random.randrange(len(mutated_genome))  # Chọn một chỉ số ngẫu nhiên để đột biến
        if random.random() <= probability:  # Đột biến chỉ với xác suất nhất định
            mutated_genome[index] = 1 - mutated_genome[index]  # Đảo bit (0 thành 1 hoặc 1 thành 0)
    return mutated_genome




