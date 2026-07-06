
# the function below performs a one mutant walk from a given genotype    
def one_mutant_walk(genotype: list):
    gene = rd.randint(0, len(genotype)-1)
    if genotype[gene] == 1:
        genotype[gene] = 0
    elif genotype[gene] == 0:
        genotype[gene]=1
    return genotype

# the following function calculates the hammond distance between two genotypes
def hammond_distance(genotype_1:list,
                     genotype_2:list):
    hammond_distance = 0
    for i in genotype_1:
        if genotype_1 != genotype_2:
            hammond_distance+=1
        else:
            pass
    return hammond_distance

def all_one_hammonds(genotype:list):
    one_hammonds = np.zeros(len(genotype), dtype = object)
    for i in genotype:
        print(i)
        temp = np.zeros(len(genotype))
        temp[:] = genotype
        if genotype[i] == 1:
            temp[i] = 0
        elif genotype[i] == 0:
            temp[i] = 1
        one_hammonds[i] = [temp]
    return one_hammonds
    

   

def one_mutant_space(diffs: list,
                    ensemble: dict,
                    rounds: int):
    random_genome_number = rd.randint(0,len(ensemble)-1)
    start_genome = ensemble[random_genome_number]
    
    current_genome = np.zeros(len(start_genome), dtype = int) 
    current_genome[:] = start_genome
    rounds_list = []
    genotype_list = [current_genome]
    temp_genome = np.zeros(len(current_genome), dtype = int)
    fitness_dict = {}
    roundd = 0
    while rounds > 0:
        rounds_list.append(roundd)
        passed = 0
        while passed == 0: 
            temp_genome[:] = one_mutant_walk(current_genome)
            one_hammonds = all_one_hammonds(current_genome)
            checked_hammonds = []
            print(f"the starting genome is {start_genome}")
            print(f"the current genome is {current_genome}")
            print(f"the temp genome is {temp_genome}")
            print(f"the one hammonds are {one_hammonds}")
            key_current = 0
            key_temp = 0
            checked = 0
            for i in checked_hammonds:
                if (temp_genome == checked_hammonds[i]).all():
                    checked = 1
            if checked == 0:
                for key, value in ensemble.items():
                    if (value == current_genome).all():
                        key_current = key
                    elif (value == temp_genome).all():
                        key_temp = key
                if diffs[key_current, key_temp] <= 0:
                    pass
                elif diffs[key_current, key_temp] > 0:
                    fitness_dict[diffs[key_current, key_temp]] = (current_genome, temp_genome)
                    current_genome[:] = temp_genome
                    temp_genome[:]=0
                    passed = 1
    return fitness_dict


def generate_mini_ensemble(N: int,
                           A: int = 2,
                           rounds: int = 10,
                           players: int = 10,
						   start: int = 10):
    ensemble = {}
    random_nums = [rd.randint(0,N) for i in range(start)]
    for i in random_nums:
        ensemble[i] = hp.generate_bit_strings(i, N, A)
    rounds_counter = 0
    while rounds_counter < rounds:
        copy_ensemble = ensemble.copy()
        for key, value in copy_ensemble.items():
            one_hammonds = all_one_hammonds(value)
            for key1, value1 in copy_ensemble.items():
                for j in one_hammonds:
                    for h in j:
                        if not (value1 == h).all():
                            ensemble[rd.randint(A*N,len(ensemble)+A*N)] = h
        rounds_counter+=1
    final_ensemble = {}
    seen = []
    for key, value in ensemble.items():
        value_tuple = tuple(value)
        if value_tuple not in seen:
            seen.append(value_tuple)
            final_ensemble[len(final_ensemble)] = value
    return final_ensemble
