from MusicalResources import pitches_and_durations_resources as pitdur

PITCH_STD_KEY_MXML = [['C', '0'], ['C', '1'], ['D', '0'], ['D', '1'], ['E', '0'], ['F', '0'], ['F', '1'], ['G', '0'], ['G', '1'], ['A', '0'], ['A', '1'], ['B', '0']]

DURATIONS = [4, 3, 2, 1]
DURATIONS_TYPE_KEY = ["half", "quarter", "quarter", "eighth"]

DYNAMICS_KEY = ['ff', 'f', 'mf', 'mp', 'p', 'pp']
DYNAMICS_KEY_SOUND = ['115', '100', '85', '70', '55', '40']

instruments = []
notes_instruments={}

def get_number_44bars(durations):
    sum_durations = 0
    for duration in durations:
        sum_durations += DURATIONS[duration]
    sum_durations -= DURATIONS[durations[-1]]
    return int(sum_durations / 8) + 1

def number_44bars():
    n_bars = []
    for instrument in instruments:
        n_bars.append(get_number_44bars(notes_instruments[instrument[1]]["duration"]))
    return min(n_bars)

def note_from_lily_to_mxml(note):
    if note!='r':
        return PITCH_STD_KEY_MXML[pitdur.convert_note_to_number(note)]
    else:
        return "r"

def notes_from_lily_to_mxml(notes):
    converted = []
    for note in notes:
        converted.append(note_from_lily_to_mxml(note))
    return converted

def add_note(namefile, note, index_dur, octave="", tie_start=False, tie_stop=False):
    f = open(namefile, 'a')
    f.write("      <note>\n")
    if note != 'r':
        f.write("        <pitch>\n")
        f.write("          <step>"+note[0]+"</step>\n")
        if note[1]!='0':
            f.write("          <alter>"+note[1]+"</alter>\n")
        f.write("          <octave>"+octave+"</octave>\n")
        f.write("        </pitch>\n")
    else:
        f.write("        <rest measure=\"no\"/>\n")
    f.write("        <duration>"+str(DURATIONS[index_dur])+"</duration>\n")
    if tie_start:
        f.write("       <tie type=\"start\"/>\n")
    if tie_stop:
        f.write("       <tie type=\"stop\"/>\n")        
    f.write("        <type>"+DURATIONS_TYPE_KEY[index_dur]+"</type>\n")
    if index_dur==1:
        f.write("        <dot/>\n")
    f.write("      </note>\n")
    f.close()

def update_measure(namefile, n_measure):
    f = open(namefile, 'a')
    n_measure += 1
    f.write("    </measure>\n")
    f.write("    <measure number=\""+str(n_measure)+"\">\n")
    f.close()
    return n_measure

def add_dynamics(namefile, note_dynamic):
    f = open(namefile, 'a')
    f.write("      <direction placement=\"below\">\n")
    f.write("        <direction-type>\n")
    f.write("          <dynamics default-y=\"-67\">\n")
    f.write("            <"+DYNAMICS_KEY[note_dynamic]+"/>\n")
    f.write("          </dynamics>\n")
    f.write("        </direction-type>\n")
    f.write("        <sound dynamics=\""+DYNAMICS_KEY_SOUND[note_dynamic]+"\"/>\n")
    f.write("      </direction>\n")
    f.close()

def fill_last_bar(namefile, beat):
    if beat % 8 < 4 and beat % 8 != 0:
        add_note(namefile, 'r', beat % 8)
        add_note(namefile, 'r', 0)
    elif beat % 8 == 4:
        add_note(namefile, 'r', 0)
    else:
        add_note(namefile, 'r', beat % 8 - 4)
    f = open(namefile, 'a')
    f.write("    </measure>\n")
    f.write("  </part>\n")
    f.close()

def header(namefile, name_composition, name_composer):
    f = open(namefile, 'w')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<!DOCTYPE score-partwise PUBLIC\n")
    f.write("    \"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n")
    f.write("    \"http://www.musicxml.org/dtds/partwise.dtd\">\n")

    f.write("<score-partwise version=\"4.0\">\n")
    f.write("  <work>\n")
    f.write("    <work-title>"+name_composition+"</work-title>\n")
    f.write("  </work>\n")
    f.write("  <identification>\n")
    f.write("    <creator type=\"composer\">"+name_composer+"</creator>\n")
    f.write("    <rights>Copyright © 2001 Recordare LLC</rights>\n")
    f.write("    <encoding>\n")
    f.write("      <encoding-date>2002-02-16</encoding-date>\n")
    f.write("      <encoder>Michael Good</encoder>\n")
    f.write("      <software>Finale 2002 for Windows</software>\n")
    f.write("      <encoding-description>MusicXML 1.0 example</encoding-description>\n")
    f.write("    </encoding>\n")
    f.write("    <source>Based on Breitkopf &amp; Härtel edition of 1895</source>\n")
    f.write("  </identification>\n")
    f.close()

def part_list(namefile):
    f = open(namefile, 'a')
    f.write("  <part-list>\n")
    f.write("    <part-group number=\"1\" type=\"start\">\n")
    f.write("       <group-symbol default-x=\"-5\">bracket</group-symbol>\n")
    f.write("       <group-barline>yes</group-barline>\n")
    f.write("    </part-group>\n")
    for instrument in instruments:
        f.write("    <score-part id=\""+instrument[0]+"\">\n")
        f.write("      <part-name>"+instrument[1]+"</part-name>\n")
        f.write("      <group>score</group>\n")
        f.write("    </score-part>\n")
    f.write("    <part-group number=\"1\" type=\"stop\"/>\n")
    f.write("  </part-list>\n")
    f.close()

    
def part(namefile, instrument, octave, clef=["G", "2"]):
    f = open(namefile, 'a')
    f.write("  <part id=\""+instrument[0]+"\">\n")
    f.write("    <measure number=\"1\">\n")
    f.write("      <attributes>\n")
    f.write("        <divisions>2</divisions>\n")
    f.write("        <key>\n")
    f.write("          <fifths>0</fifths>\n")
    f.write("        </key>\n")
    f.write("        <time>\n")
    f.write("          <beats>4</beats>\n")
    f.write("          <beat-type>4</beat-type>\n")
    f.write("        </time>\n")
    f.write("        <clef>\n")
    f.write("          <sign>"+clef[0]+"</sign>\n")
    f.write("          <line>"+clef[1]+"</line>\n")
    f.write("        </clef>\n")
    f.write("      </attributes>\n")
    f.close()

    beat = 0
    last_beat = 0
    n_measure = 1
    n_max_measures = number_44bars()
    last_dynamic = 1000
    for index in range(len(notes_instruments[instrument[1]]["pitch"])-1):
        note_aux = note_from_lily_to_mxml(notes_instruments[instrument[1]]["pitch"][index])
        index_dur_aux = notes_instruments[instrument[1]]["duration"][index]
        note_dynamic_aux = notes_instruments[instrument[1]]["dynamic"][index]
        
        last_beat = beat
        beat += DURATIONS[index_dur_aux]
        
        if note_aux != "r" and (last_dynamic==None or last_dynamic!=note_dynamic_aux):
            add_dynamics(namefile, note_dynamic_aux)
        
        if last_beat % 8 > beat % 8 and beat % 8 == 0:
            add_note(namefile, note_aux, index_dur_aux, octave)
            n_measure = update_measure(namefile, n_measure)
        elif last_beat % 8 > beat % 8 and beat % 8 != 0:
            add_note(namefile, note_aux, last_beat % 8 - 4, octave, tie_start=True)
            n_measure = update_measure(namefile, n_measure)
            add_note(namefile, note_aux, 4 - beat % 8, octave, tie_stop=True)    
        else:
            add_note(namefile, note_aux, index_dur_aux, octave)
        last_dynamic = note_dynamic_aux
        if(n_measure==n_max_measures):
            break
        
    fill_last_bar(namefile, beat)

def end(namefile):
    f = open(namefile, 'a')
    f.write("</score-partwise>\n")
    f.close()

def make_file(namefile, name_composition, name_composer, octaves, clefs):
    header(namefile, name_composition, name_composer)
    part_list(namefile)
    for i in range(len(instruments)):
        part(namefile, instruments[i], octaves[i], clefs[i])
    end(namefile)
