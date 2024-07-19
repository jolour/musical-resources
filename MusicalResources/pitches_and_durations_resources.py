import copy
import random

PITCH_STD_KEY = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']
DURATIONS_KEY_STD = range(1,13)

def get_row(matrix, i):
    """
    This function returns the ith row of a given matrix
    """
    return matrix[i]

def get_column(matrix, j):
    """
    This function returns the jth column of a given matrix
    """
    col_aux = []
    for i in range(len(matrix[0])):
        col_aux.append(matrix[i][j]) 
    return col_aux

def convert_number_to_note(note, notes_key=PITCH_STD_KEY):
    """
    This function converts a pitch in a number to a note
    """
    if type(note) == int:
        return notes_key[note % 12]
    elif type(note) == str:
        return note 

def convert_numbers_to_notes(row, notes_key=PITCH_STD_KEY):
    """
    This function converts a row in numbers to a row in notes
    """
    if type(row[0]) == int:
        row_aux = []
        for n_row in row:
            row_aux.append(convert_number_to_note(n_row, notes_key))
        return row_aux
    elif type(row[0]) == str:
        return row

def convert_note_to_number(note, notes_key=PITCH_STD_KEY):
    """
    This function converts a pitch in a note to a number
    """
    if type(note) == str:
        for number, note_aux in enumerate(notes_key):
            if note == note_aux:
                return number
    elif type(note) == int:
        return note 
    

def convert_notes_to_numbers(row, notes_key=PITCH_STD_KEY):
    """
    This function converts a row in notes to a row in numbers
    """
    if type(row[0]) == str:
        row_aux = []
        for note in row:
            row_aux.append(convert_note_to_number(note, notes_key))
        return row_aux
        #if len(row_aux) == len(row):
        #    return row_aux
        #else:
        #    print('There was a problem, not all elements were converted. \nCorrect the typos in the notes names.')
    elif type(row[0]) == int:
        return row

def get_index_of_note_in_row(note, row):
    """
    This function returns the index where a given note appears in a given row
    """
    if type(note) == int:
        note = convert_number_to_note(note)
    if type(row[0]) == int:
        row = convert_numbers_to_notes(row)
    for index, note_row in enumerate(row):
        if note_row == note:
            return index

def transpose(row, i = 0, mod_yes = True):
    """
    This function transposes a row up i half-tones in relative (by default) or absolute pitches (fot mod_yes=False) 
    """
    row_aux = convert_notes_to_numbers(row)
    if mod_yes:
        transposed = [(x + i) % 12 for x in row_aux]
    else:
        transposed = [(x + i) for x in row_aux]
    return transposed

def transpose_all(row):
    """
    This function returns a matrix with all 12 transpositions of the original row
    """
    transposed_all = []
    for i in range(12):
        transposed_all.append(transpose(row, i))
    return transposed_all

def retrograde(row_given, i = 0, mod_yes = True):
    """
    This function retrogrades a row and transposes it up i half-tones in relative (by default) or absolute pitches (fot mod_yes=False) 
    """
    if type(row_given[0]) == str:
        row = convert_notes_to_numbers(row_given)
        print(row)
    else:
        row = row_given
    n_row = len(row)
    if mod_yes:
        retrograded = [(row[n_row-1-row_i] + i) % 12 for row_i in range(n_row)]
    else:
        retrograded = [(row[n_row-1-row_i] + i) for row_i in range(n_row)]
    if type(row_given[0]) == str:
        retrograded = convert_numbers_to_notes(retrograded)
    return retrograded

def retrograde_all(row):
    """
    This function returns a matrix with all 12 transpositions of the retrograded row
    """
    retrograded_all = []
    for i in range(12):
        retrograded_all.append(retrograde(row, i))
    return retrograded_all

def invert(row, i = 0, mod_yes = True):
    """
    This function  a matrix with all 12 transpositions of a row
    """
    row_aux = convert_notes_to_numbers(row)
    if mod_yes:
        inverted = [(2*row_aux[0] - x + i) % 12 for x in row_aux]
    else:
        inverted = [(2*row_aux[0] - x + i) for x in row_aux]
    return inverted

def invert_all(row):
    """
    This function returns a matrix with all 12 transpositions of the inverted row
    """
    inverted_all = []
    for i in range(12):
        inverted_all.append(invert(row, i))
    return inverted_all

def matrix(row):
    """
    This function returns a matrix with all 12 transpositions of the inverted row
    """
    row_aux = convert_notes_to_numbers(row)
    matrix = []
    for i in row_aux:
        matrix.append(convert_numbers_to_notes(transpose(row_aux, i-row_aux[0])))
    return matrix

def matrix_inv(row):
    row_aux = invert(convert_notes_to_numbers(row))
    matrix = []
    for i in row_aux:
        matrix.append(convert_numbers_to_notes(transpose(row_aux, i-row_aux[0])))
    return matrix

def create_12_tone_matrix(row, in_notes=False):
    """
    This function returns the dodecaphonic matrix of a given row
    """
    row_aux = convert_notes_to_numbers(row)
    interval_sequence = [x - row_aux[0] for x in row_aux]
    matrix_aux = [[ (row_aux[0] + interval_across - interval_down ) % 12
            for interval_across in interval_sequence] 
            for interval_down in interval_sequence]
    if in_notes:
        return [convert_numbers_to_notes(row_aux) for row_aux in matrix_aux]
    else:
        return matrix_aux
    
def print_matrix(matrix):
    """
    This function prints a given matrix
    """
    print(*matrix, sep = "\n")

def get_notes_around(matrix_notenames, notes_key=PITCH_STD_KEY):
    """
    This function returns the notes that are directly around (below, above, left and right) a given note in the serial matrix
    """
    dictionary = {}
    for note in notes_key:
        dictionary[note] = set()
    for i in range(12):
        for j in range(12):
            for note in notes_key:
                if matrix_notenames[i][j] == note:         
                    dictionary[note].update([matrix_notenames[(i - 1) % 12][j]])
                    dictionary[note].update([matrix_notenames[(i + 1) % 12][j]])
                    dictionary[note].update([matrix_notenames[i][(j - 1) % 12]])
                    dictionary[note].update([matrix_notenames[i][(j + 1) % 12]])
    return dictionary

def print_notes_around(matrix_notenames, notes_key=PITCH_STD_KEY):
    """
    This function prints the results of the function get_notes_around
    """
    philosophia_dict = get_notes_around(matrix_notenames, notes_key)
    for note in philosophia_dict:
        print(note, 'is surrounded by', sorted(philosophia_dict[note]))

def matrix_durations(matrix, durations_key, scaling_factor = 1):
    row_in_notes = False
    if type(matrix[0][0]) == str:
        row_in_notes = True
    matrix_aux = copy.deepcopy(matrix)
    for i in range(12):
        if row_in_notes:
            row_matrix_aux = convert_notes_to_numbers(matrix_aux[i])
        for j in range(12):
            if row_in_notes:
                x = row_matrix_aux[j]
            else:
                x = matrix_aux[i][j]
            if x in range(12):
                matrix_aux[i][j] = durations_key[x]*scaling_factor
            else:     
                print("Wrong number detected!", x)
                return
    return matrix_aux

def get_correspondence_row(row):
    row_aux = convert_notes_to_numbers(row)
    correspondence_row = [0] * 12
    for i in range(12):
        correspondence_row[row_aux[i]] = i + 1 
    return correspondence_row

def matrix_durations_from_chromatic(matrix, scaling_factor = 1):
    return matrix_durations(matrix=matrix, 
                            durations_key=DURATIONS_KEY_STD, 
                            scaling_factor=scaling_factor)    

def matrix_durations_from_serie(matrix, scaling_factor = 1):
    return matrix_durations(matrix=matrix, 
                            durations_key=get_correspondence_row(convert_notes_to_numbers(matrix[0])), 
                            scaling_factor=scaling_factor)    

def interval_differences_in_half_tones(row):
    if type(row[0]) == str:
        row_aux = convert_notes_to_numbers(row)
    else:
        row_aux = row
    interval_sequence = []
    for i in range(11):
        i=i+1
        interval_sequence.append((row_aux[i] - row_aux[i-1]) % 12)
    return interval_sequence

def get_sum_duration_notes(notes, row_notes, matrix_durations):
    list_sum = []
    list_sum_r = []
    for i, row_durations in enumerate(matrix_durations):
        sum = 0
        sum_r = 0
        for note in notes:
            sum += row_durations[get_index_of_note_in_row(note, row_notes)]
            sum_r += row_durations[-1 -get_index_of_note_in_row(note, row_notes)]
        print('linha', i+1, '- p:', sum, '  r:', sum_r)
        list_sum.append(sum)
        list_sum_r.append(sum_r)
    #print([x for x in enumerate(sorted(list_sum, reverse=True))])
    #mapping = {k : i for i, k in enumerate(sorted(list_sum, reverse=True))}
    #print(mapping)
    #print([mapping[i] for i in list_sum])

def random_lengths(n_pitches, min_length=1, max_length=12):
    lengths_phrases=[]
    n_durations = 0
    while n_durations < n_pitches:
        length = random.randint(min_length, max_length)
        lengths_phrases.append(length)
        n_durations += length
    n_phrases = len(lengths_phrases)
    lengths_phrases[n_phrases-1] = lengths_phrases[n_phrases-1] - (n_durations - n_pitches)
    return lengths_phrases

def random_durations(number, probabilities=[0.1, 0.2, 0.3, 0.4]):
    durations=random.choices(range(4), probabilities, k=number)
    return durations

def random_dynamics(n_pitches, min_length=1, max_length=12):
    dynamics = random_lengths(n_pitches, min_length, max_length)
    sum_aux = 0
    for index in range(len(dynamics)):
        dynamics[index] = [dynamics[index], random.randint(0, 5)]
        sum_aux += dynamics[index][0]
    if sum_aux != n_pitches:
        print("ERROR in random_dynamics")
        exit
    return dynamics

def update_dynamic(note_dynamic, expanded, index, aux):
    expanded.append(note_dynamic[1])
    if aux == note_dynamic[0]:
        aux = 1
        index += 1
    elif aux < note_dynamic[0]:
        aux += 1
    return expanded, index, aux

def from_pitches_to_notes(pitches, lengths_phrases, note_dynamic):
    note_name = []
    aux = 0
    expanded = []
    index_dynamic = 0
    dynamic_aux = 1
    for length in lengths_phrases:
        for _ in range(length):
            note_name.append(pitches[aux])
            aux+=1
            expanded, index_dynamic, dynamic_aux = update_dynamic(note_dynamic[index_dynamic], expanded, index_dynamic, dynamic_aux)        
        note_name.append('r')
        expanded.append(None)      
    return note_name, expanded

def build_sequence_sets(sets):
    name_set = []
    for set_cur in sets:
        name_set.append(set_cur[0])
    return name_set

def build_sequence_pitches(sets):
    note_pitch = []
    for set_pitch in sets:
        for pitch in set_pitch[1]:
            note_pitch.append(pitch)
    return note_pitch

def generate_melody(sets, probabilities=[0.1, 0.2, 0.3, 0.4], range_length_phrases=[1,8], range_length_dynamics=[3,12]):
    pitches = build_sequence_pitches(sets)
    n_pitches = len(pitches)
    lengths_phrases = random_lengths(n_pitches, range_length_phrases[0], range_length_phrases[1])
    note_duration = random_durations(n_pitches + len(lengths_phrases), probabilities)
    note_dynamic = random_dynamics(n_pitches, range_length_dynamics[0], range_length_dynamics[1])
    note_name, note_dynamic_expanded = from_pitches_to_notes(pitches, lengths_phrases, note_dynamic)
    return lengths_phrases, note_duration, note_name, note_dynamic, note_dynamic_expanded