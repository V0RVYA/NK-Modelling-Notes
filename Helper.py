import numpy as np
import random as rd

def generate_weights_random(N: int,
                     K: int,
                     ensemble: dict,
                     A: int = 2):
    if random == True:
        weights = {}
        for i in range(N):
            weight_i = []
            for j in range(len(ensemble)):
                weight_i.append(rd.random())
            weights[i] = weight_i
        return weights, ensemble

# This assigns K epistatically affecting neighbours to each gene i in N and returns a dictionary of all epistatic connections keyed for each node
def assign_neighbours(N: int,
                      K: int):
    #here we will do the simplest version, where each locus i is impacted by K loci that come after it
    #therefore epistatic interactions will be modelled as one way
    # will use this to contrast to a purely statistical modelling of the weight assignment
    K_loci = {}
    for i in range(N):
        temp = []
        for j in range(K+1):
            h = i + j
            if h >= N:
                y = N-h
                if y == 0:
                    temp.append(y)
                elif y < 0:
                    temp.append(-y)
            elif h < N:
                temp.append(h)
        K_loci[i] = temp
    return K_loci


# This generates a full ensemble of all possible N length genotypes, with A possible alleles for each gene i => DO NOT use for large N
def generate_ensemble(N: int,
                      A: int = 2):   
    ensemble = {}
    for i in range(A**N):
        bit_string = np.zeros(N, dtype=int)
        j = i
        length = 0
        while j > 0:
            h = j % A
            bit_string[length] = h
            length += 1
            j //= A
        ensemble[i] = bit_string
    return ensemble 


# generate genomes as bit strings
def generate_bit_strings(number: int,
                         N: int,
                         A: int):
    bit_string = np.zeros(N, dtype=int)
    j = number
    position = 0
    while j > 0 and position < N:
        bit = j%A
        bit_string[position] = bit
        position += 1
        j //= A
    return bit_string

# Find all the one hammond moves from a given position
def all_one_hammonds(genotype:list):
    one_hammonds = np.zeros(len(genotype), dtype = object)
    for i in range(len(genotype)):
        temp = genotype.copy()
        if genotype[i] == 1:
            temp[i] = 0
        elif genotype[i] == 0:
            temp[i] = 1
        one_hammonds[i] = [temp]
    return one_hammonds

    
# given all the one hammond distance genomes, this returns their key in the ensemble space for fitness matching
def hammonds_keys(hammonds: list,
                  ensemble: dict):
    hammond_keys = np.zeros(len(hammonds), dtype=int)
    for i in range(len(hammonds)):
        for key, value in ensemble.items():
            if (value == hammonds[i]).all():
                hammond_keys[i] = key
    return hammond_keys

# given a list of keys to the ensemble, fitnesses and the current genomes fitness, return the neighbours that are higher fitness
def good_neighbours(hammond_keys: list,
                    ensemble: dict,
                    fitnesses: list,
                    fitness_current: float):

    hammond_fitness = []
    good_neighbours = []

    for k in hammond_keys:
        hammond_fitness.append((ensemble[k], fitnesses[k]))
    for j in hammond_fitness:
        genome, fitness = j
        if fitness - fitness_current > 0:
            good_neighbours.append(j)
    return good_neighbours

