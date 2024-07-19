DURATIONS = [2, 1.5, 1, 0.5]
DURATIONS_KEY = ['2', '4.', '4', '8']

DYNAMICS_KEY = ['\\ff', '\\f', '\\mf', '\\mp', '\\p', '\\pp']

instruments = []

def header(namefile, name_composition, name_composer):
    f = open(namefile, 'w')
    f.write("\\version \"2.24.3\"\n\n")
    f.write("\\header {\n title = \""+name_composition+"\"\n")
    f.write(" composer = \""+name_composer+"\"\n}")
    f.write("\n\n")
    f.write("global = {\n \\time 4/4\n \\key c \\major\n \\tempo 4 = 120\n}")
    f.write("\n\n")
    f.close()

def add_note(melody_lily, note_aux, octave=""):
    melody_lily += note_aux
    if note_aux != "r":
        melody_lily += octave
    return melody_lily
            
def add_duration(melody_lily, duration_index, last_dur_index):
    if last_dur_index!=duration_index:
        melody_lily += DURATIONS_KEY[duration_index]
    return melody_lily

def add_dynamic(melody_lily, note_name, note_dynamic, last_dynamic):
    if note_name != "r" and (last_dynamic==None or last_dynamic!=note_dynamic):
        melody_lily += DYNAMICS_KEY[note_dynamic]
    return melody_lily

def get_dur_index(duration):
    return 4 - int(duration*2)

def fill_last_bar(melody_lily, beat):
    if beat % 4 == 0:
        melody_lily += 'r1'
    elif beat % 4 < 2:
        melody_lily += 'r'
        melody_lily += DURATIONS_KEY[get_dur_index(2 - beat % 4)]
        melody_lily += 'r2'
    elif beat % 4 == 2:
        melody_lily += 'r2'
    else:
        melody_lily += 'r'
        melody_lily += DURATIONS_KEY[get_dur_index(4 - beat % 4)]
    melody_lily += " \\bar \"|.\""
    return melody_lily

def melody_str(notes_instruments, instrument, octave):
    melody_lily=str()
    n_durations = len(notes_instruments[instrument[1]]["pitch"])
    
    beat = 0
    last_beat = 0
    last_dur_index = -1
    last_dynamic = 1000
    
    for index in range(n_durations-1):
        note_aux = notes_instruments[instrument[1]]["pitch"][index]
        index_dur_aux = notes_instruments[instrument[1]]["duration"][index]
        note_dynamic_aux = notes_instruments[instrument[1]]["dynamic"][index]
        
        last_beat = beat
        beat += DURATIONS[index_dur_aux]    
        
        melody_lily = add_note(melody_lily, note_aux, octave)
        if last_beat % 4 > beat % 4 and beat % 4 == 0:
            melody_lily = add_duration(melody_lily, index_dur_aux, last_dur_index)    
            melody_lily = add_dynamic(melody_lily, note_aux, note_dynamic_aux, last_dynamic)
            melody_lily += " | "
            last_dur_index = index_dur_aux
        elif last_beat % 4 > beat % 4 and beat % 4 != 0:
            melody_lily = add_duration(melody_lily, get_dur_index(4 - last_beat % 4), last_dur_index)    
            if note_aux != "r":
                melody_lily += "~"
            melody_lily = add_dynamic(melody_lily, note_aux, note_dynamic_aux, last_dynamic)
            melody_lily += " | "
            melody_lily = add_note(melody_lily, note_aux, octave)
            melody_lily = add_duration(melody_lily, get_dur_index(beat % 4), get_dur_index(4 - last_beat % 4))
            melody_lily += " "
            last_dur_index = get_dur_index(beat % 4)
        else:
            melody_lily = add_duration(melody_lily, index_dur_aux, last_dur_index)
            melody_lily = add_dynamic(melody_lily, note_aux, note_dynamic_aux, last_dynamic)
            melody_lily += " "
            last_dur_index = index_dur_aux
        last_dynamic = note_dynamic_aux
    
    melody_lily = fill_last_bar(melody_lily, beat)
    return melody_lily

def melody(namefile, melody, name_instrument, clef, relative=[False, ""]):
    f = open(namefile, 'a')
    instruments.append(["instrument"+chr(65 + len(instruments)), name_instrument])
    f.write(instruments[-1][0] + " = ")
    f.write("\\new Voice ")
    if relative[0]:
        f.write("\\relative "+relative[1]+" ")
    f.write("{\n \\clef " + clef + "\n "+melody+"\n}")
    f.write("\n\n")
    f.close()

def score(namefile):
    f = open(namefile, 'a')
    f.write("\\score {\n \\new StaffGroup << \n")
    for instrument in instruments:
        f.write("  \\new Staff \\with { midiInstrument = \"" + instrument[1] + "\" } \n")
        f.write("  << \\global \\" + instrument[0] + " >>\n")
    f.write(" >>\n \\layout { }\n \\midi { }\n}")
    f.write("\n\n")
    f.close()    