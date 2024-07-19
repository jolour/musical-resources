import math
import random
import copy
from MusicalResources import pitches_and_durations_resources as pitdur

DOMAIN_NUMBER=['I', 'II', 'III', 'IV', 'V']

def build_sets(row, pitch_distribution):
    """
    This function returns the sets of a given row destributed according to a pitch distribution
    """
    sets = []
    k = 0
    row_aux = pitdur.convert_notes_to_numbers(row)
    for number_notes in pitch_distribution:
        set_aux = []
        for _ in range(number_notes):
            set_aux.append(row_aux[k])
            k+=1
        set_aux = sorted(set_aux)
        sets.append([set_aux, pitdur.convert_numbers_to_notes(set_aux)])    
    return sets

def set_multiplication(set1, set2, multiplication_ref_note):
    res_multiplication = set()
    for note_set2 in set2:
        for note_set1 in set1:
            res_multiplication.update([(note_set2 + note_set1 - multiplication_ref_note)])
    return sorted(res_multiplication)

def build_derived_sets(row, pitch_distribution, reference_note = [], 
                       convert_names = False, using_set=False):
    row_aux = pitdur.convert_notes_to_numbers(row)
    sets = [x[0] for x in build_sets(row_aux, pitch_distribution)]
    if reference_note == []:
        ref_note = sets[0][0]
    else:
        ref_note = pitdur.convert_notes_to_numbers(reference_note)[0]
    dict_sets = {}
    
    for i, set1 in enumerate(sets):
        if convert_names:
            if using_set:
                dict_sets[chr(65 + i)] = set(pitdur.convert_numbers_to_notes(set1))
            else:
                dict_sets[chr(65 + i)] = [set1, pitdur.convert_numbers_to_notes(set1)]
        else:
            dict_sets[chr(65 + i)] = set1
    
    for i, set1 in enumerate(sets):
        for j, set2 in enumerate(sets):
            set_aux = set_multiplication(set1, set2, ref_note)
            if convert_names:
                if using_set:
                    dict_sets[chr(65 + i) + chr(65 + j)] = set(pitdur.convert_numbers_to_notes(set_aux))
                else:
                    dict_sets[chr(65 + i) + chr(65 + j)] = [set_aux, pitdur.convert_numbers_to_notes(set_aux)]
            else:
                if using_set:
                    dict_sets[chr(65 + i) + chr(65 + j)] = set(set_aux)
                else:
                    dict_sets[chr(65 + i) + chr(65 + j)] = set_aux
    return dict_sets

def print_all_sets(dict_sets, using_set=False):
    for set_name in dict_sets:
        if type(dict_sets[set_name]) == set:
            print(set_name, '-', dict_sets[set_name])
        elif type(dict_sets[set_name][0]) == list and not using_set:
            print(set_name, '-', dict_sets[set_name][0], '=', dict_sets[set_name][1])
        elif type(dict_sets[set_name][0]) == list and using_set:
            print(set_name, '-', set(dict_sets[set_name][1]))
        else:
            print(set_name, '-', dict_sets[set_name])

def print_multiplication_rules_for_derived_sets(row, pitch_distribution):
    row_aux = pitdur.convert_notes_to_numbers(row)
    sets = build_derived_sets(row_aux, pitch_distribution, convert_names=True)
    for set_name in sets:
        if len(set_name) == 2:
            print(set_name[0], "x", set_name[1], "=", set_name)
            print(sets[set_name[0]][1], "x", sets[set_name[1]][1], "=", sets[set_name][1])        

def counterclockwise_rotation(distribution):
    n_distribution = len(distribution)
    distribution_aux = [0] * n_distribution
    distribution_aux[-1] = distribution[0]
    for iter in range(n_distribution - 1): 
        distribution_aux[iter] = distribution[iter+1]
    return distribution_aux

def clockwise_rotation(distribution):
    n_distribution = len(distribution)
    distribution_aux = [0] * n_distribution
    distribution_aux[0] = distribution[-1]
    for iter in range(n_distribution - 1): 
        distribution_aux[iter+1] = distribution[iter]
    return distribution_aux

def change_octaves(row, octaves):
    new_row = []
    n = len(row)
    for i in range(n):
        new_row.append(row[i] + 12 * octaves[i])
    return new_row

def build_harmonic_domains(row, pitch_distribution, retrograde_distribution,
                           ref_notes=[], 
                           convert_names = False, using_set=False):
    dict_domains = {}
    if retrograde_distribution:
        pitch_distribution_aux = pitdur.retrograde(pitch_distribution)
    else:
        pitch_distribution_aux = pitch_distribution
    for i in range(len(pitch_distribution_aux)):
        if ref_notes == []:
            domain_aux = build_derived_sets(row=row,
                                  pitch_distribution=pitch_distribution_aux, 
                                  convert_names=convert_names,
                                  using_set=using_set)
        else:
            domain_aux = build_derived_sets(row=row,
                                  pitch_distribution=pitch_distribution_aux, 
                                  convert_names=convert_names, 
                                  reference_note=ref_notes[i],
                                  using_set=using_set)
        domain_name = 'Domain ' + DOMAIN_NUMBER[i] + ' - ' + str(pitch_distribution_aux)
        dict_domains[domain_name] = domain_aux
        if retrograde_distribution:
            pitch_distribution_aux = clockwise_rotation(pitch_distribution_aux)
        else:
            pitch_distribution_aux = counterclockwise_rotation(pitch_distribution_aux)
    return dict_domains

def print_harmonic_domains(dict_domains, using_set=False):
    for domain_name in dict_domains:
        print(domain_name,'\n')
        print_all_sets(dict_domains[domain_name], using_set=using_set)
        print('\n')    

def print_sets_in_matrix_form(dict_sets):
    n_sets=0
    for set_name in dict_sets:
        if len(set_name) == 1:
            dict_sets_aux = dict_sets[set_name]
            if type(dict_sets_aux) == set:
                print(set_name, '-', sorted(dict_sets_aux), end='\t\t')
            elif type(dict_sets_aux[0]) == list:
                print(set_name, '-', sorted(set(dict_sets_aux[1])), end='\t\t')
            else:
                print(set_name, '-', sorted(set(dict_sets_aux)), end='\t\t')
            n_sets +=1 
    print('\n')
    for i in range(n_sets):
        print('\t', f"{chr(65+i) : ^62}", end=' ')
    for i in range(n_sets):
        print('\n', chr(65 + i), end='\t')
        for j in range(n_sets):
            set_name = chr(65 + i) + chr(65 + j)
            dict_sets_aux = dict_sets[set_name]
            if type(dict_sets_aux) == set:
                print(sorted(dict_sets_aux), end='\t')
            elif type(dict_sets_aux[0]) == list:
                f_string = f"{*sorted(set(dict_sets_aux[1])),}"
                x = (75//8-len(f_string)//8)
                print(f_string, end='\t'*x)
            else:
                print(sorted(set(dict_sets_aux)), end='\t')

def print_harmonic_domains_in_matrix_form(dict_domains):
    for domain_name in dict_domains:
        print(domain_name,'\n')
        print_sets_in_matrix_form(dict_domains[domain_name])
        print('\n')

def find_all_sets(dict_sets, subset):
    sets_found = []
    names_sets_found = []
    for set_name in dict_sets:
        if type(dict_sets[set_name][0]) == list:
            dict_set_aux = dict_sets[set_name][1]
        else:
            dict_set_aux = pitdur.convert_numbers_to_notes(dict_sets[set_name])
        if subset <= set(dict_set_aux):
            names_sets_found.append(set_name)
            sets_found.append(set(dict_set_aux))
    return names_sets_found, sets_found

def find_harmonic_domains(dict_domains, given_sets):
    print_found = False
    if type(given_sets) == set:
        for domain_name in dict_domains:
            names_sets_found, sets_found = find_all_sets(dict_sets=dict_domains[domain_name], subset=given_sets)
            if names_sets_found!=[]:
                if not print_found:
                    print(given_sets, 'found in the following sets:\n')
                    print_found = True
                print(domain_name,'\n')
                for (name_sets_found, set_found) in zip(names_sets_found, sets_found):
                    print(name_sets_found, '-', sorted(set_found))
                print('\n')
        if not print_found:
            print(given_sets, 'was not found.\n')    
    elif type(given_sets) == list:
        return 0
    
def print_sets_in_sequence(dict_domains, sequence_names, domain_name):
    for set_name in sequence_names:
        print(set_name, '-', sorted(set(dict_domains[domain_name][set_name][1])))

def get_number_sets(c):
    a = 1
    b = 1
    c = - c
    return round( ( -b + math.sqrt(b*b-4*a*c) ) / ( 2*a ) )

def random_sets(n_sets, dict_domains, n_domain=0):
    sets = []
    if n_domain==0:
        n_domain = random.randint(1, len(dict_domains))
    domain_names = list(dict_domains.keys())
    domain = dict_domains[domain_names[n_domain]]
    max = get_number_sets(len(domain)) - 1
    i = random.randint(0, max)
    j = random.randint(0, max)
    for _ in range(n_sets):
        aux_set = list(copy.deepcopy(domain[chr(65 + i) + chr(65 + j)]))
        random.shuffle(aux_set)
        sets.append([chr(65 + i) + chr(65 + j), aux_set])
        new_i = i
        new_j = j
        while new_i==i and new_j == j:
            new_i = i + random.randint(-1, 1) 
            new_j = j + random.randint(-1, 1) 
        i = new_i % (max + 1)
        j = new_j % (max + 1)
    return sets
