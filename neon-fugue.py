from showscore import show
import music21 as m21

score = m21.corpus.parse('beethoven/opus133.mxl')
score = score.measures(0, 10) # big score so cut it down!

part_colors = {
    "1st Violin": "#2BFA4A",
    "2nd Violin": "#E0218A",
    "Viola": "#942BFF",
    "Cello": "#04D9FF",
}

for part in score.parts:
    
    color = part_colors[part.partName]
    for n in part.recurse().getElementsByClass(m21.note.NotRest):
        if isinstance(n, m21.chord.Chord):
            # this is needed if the chord is modified e.g. .chordify()
            for subnote in n.notes:
                subnote.style.color = color
        else:
            n.style.color = color

show(score, osmd_options={"darkMode": True, "drawTitle": False}, engraving_rules={"DefaultColorMusic": "#CCCCCC"})








