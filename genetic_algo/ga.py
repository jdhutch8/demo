import json
import random

def fitness(generation, data, max_budget):
    fit_gen = {}
    for individual in generation:
        total_cost = 0
        total_vaccinated = 0
        list_of_fit_gen = []
        genome_id = max(fit_gen.keys()) + 1 if len(fit_gen.keys()) != 0 else 0  
        for count, key in enumerate(data.keys()):
            if individual[count] == 1:
                list_of_fit_gen.append(key)
                total_cost += data[key]['cost']
                total_vaccinated += data[key]['vaccinated']
        if total_cost <= max_budget and list_of_fit_gen != []:
            fit_gen[genome_id] = {'total_cost': total_cost,                        \
                                                'total_vaccinated': total_vaccinated,           \
                                                'genome': individual,                           \
                                                'weight': 0,                                    \
                                                'fitness': 1}
        else:
            fit_gen[genome_id] = {'total_cost': 0,                        \
                                                'total_vaccinated': 0,           \
                                                'genome': individual,                           \
                                                'weight': 0,                                    \
                                                'fitness': 0}
    return fit_gen

def create_weights(fit_gen, max_possible_vaccinated):
    for individual in fit_gen.keys():
        fit_gen[individual]['weight'] = (fit_gen[individual]['total_vaccinated'] / max_possible_vaccinated) 
    return fit_gen

def select_best_options(n, weighted_gen):
    parents = {}
    while len(parents.keys()) < n:
        for individual in weighted_gen.keys():
            if weighted_gen[individual]['fitness'] == 1:
                if weighted_gen[individual]['weight'] > (random.randint(0, 100) / 100):
                    if individual not in parents.keys() and len(parents.keys()) < n:
                        parents[individual] = weighted_gen[individual]
    return parents

def calculate_max_possible_vaccinated(data):
    total_possible_vaccinated = 0
    for key in data.keys():
        total_possible_vaccinated += data[key]['vaccinated']
    return total_possible_vaccinated

def mutation(individual):
    mutated_location = False
    mutated_bit = False
    for count, bit in enumerate(individual):
        if random.randint(1, 100) == 1:
            mutated_location = count
            mutated_bit = 1 if bit == 0 else 0
            individual[mutated_location] = mutated_bit 
    if mutated_location:
        return individual 
    else:
        return individual

def crossover(next_generation_dict):
    gene_a = []
    gene_b = []
    gene_a_prime = []
    gene_b_prime = []
    for count, key in enumerate(next_generation_dict.keys()):
        if count == 0: 
            gene_a = next_generation_dict[key]['genome']
        else:
            gene_b = next_generation_dict[key]['genome']
    gene_a_prime = gene_a[:2] + gene_b[2:]
    gene_b_prime = gene_b[:2] + gene_a[2:]
    next_generation = [gene_a_prime, gene_b_prime]
    return next_generation

def remove_weakest_individuals(weighted_gen):
    next_generation = [weighted_gen[individual]['genome'] for individual in weighted_gen.keys()]
    to_delete = []
    fitness_is_zero = []
    for individual in weighted_gen.keys():
        if weighted_gen[individual]['fitness'] == 0:
            fitness_is_zero.append(weighted_gen[individual]['genome'])

    lowest_num_vaccines = []
    lowest_vaccine_num = 100
    lowest_vaccine_genome = '' 
    higest_cost_vaccines = []
    higest_cost = 0
    higest_cost_genome = ''
    for i in range(2):
        for individual in weighted_gen.keys():
            if weighted_gen[individual]['fitness'] == 1:
                if weighted_gen[individual]['total_vaccinated'] < lowest_vaccine_num:
                    lowest_vaccine_genome = weighted_gen[individual]['genome']
                if weighted_gen[individual]['total_cost'] > higest_cost:
                    higest_cost_genome = weighted_gen[individual]['genome']
        lowest_num_vaccines.append(lowest_vaccine_genome)
        higest_cost_vaccines.append(higest_cost_genome)
    to_delete = fitness_is_zero + lowest_num_vaccines + higest_cost_vaccines
    if to_delete:
        for i in range(2):
            del next_generation[next_generation.index(to_delete[i])]
    else:
        for i in range(2):
            del next_generation[next_generation.index(random.randint(0, len(next_generation) - 1))]
    return next_generation

def process_generation(generation, data, max_budget, max_possible_vaccinated, population_size):
    #Process all scoring and weighting
    fit_gen = fitness(generation, data, max_budget)
    weighted_gen = create_weights(fit_gen, max_possible_vaccinated)
    #Select n best parents
    parents = select_best_options(2, weighted_gen)
    #Process crossover on children
    children = crossover(parents)
    #Remove weakest members from next generation
    next_generation = remove_weakest_individuals(weighted_gen)
    #Allow for mutation
    next_generation = list(map(mutation, next_generation))
    #Add children to next generation
    next_generation += children
    return next_generation
    
def main():
    max_budget = 100
    population_size = 50
    with open('covid.json') as json_file:
        data = json.load(json_file)
    len_gen_code = len(data.keys())

    max_possible_vaccinated = calculate_max_possible_vaccinated(data)
    next_generation = [[random.randint(0, 1)
                for j in range(len_gen_code)] for i in range(population_size)]
    next_generation = map(mutation, next_generation)
    optimal_solution_found = False
    generations = 0
    while not optimal_solution_found: 
        next_generation = process_generation(next_generation, data, max_budget, max_possible_vaccinated, population_size)
        fitness_next_gen = fitness(next_generation, data, max_budget)
    
        print(f"\nGeneration {generations}")
        for key in fitness_next_gen.keys():
            if fitness_next_gen[key]['fitness']:
                print("\t", fitness_next_gen[key]['genome'], fitness_next_gen[key]['total_vaccinated'])
                if fitness_next_gen[key]['total_vaccinated'] == 18:
                    optimal_solution_found = True
                    print(fitness_next_gen[key])
        generations += 1
        if generations == 200:
            break

    print("length next gen", len(next_generation))
if __name__=='__main__':
    main()
