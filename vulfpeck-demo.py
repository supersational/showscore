import music21
from showscore import show

abc = """
X:1
T:Wait for the Moment
C:Jack Stratton
L:1/4
Q:1/4=79
M:4/4
K:C
V:1 clef=treble
z "C" [G,CE]"E7" .[^G,DE] z | z"Am7" [G,CE]"Gm" [G,_B,D]"C" .[G,CE] | z"F" [F,A,C]"C/E" .[E,G,C] z | %3
 z"Dm7" [D,F,A,C]"C/G" [G,CE]"G" .[G,B,D] | %4
V:2 bass
 C, .E, z | z A,, G,, .C, | z F,, .E,, z | z D,, G,, .G,, | %4
"""

# Create a music21 stream from the ABC string
score = music21.converter.parse(abc, format="abc")

# Correct the clef
score.parts[0].measure(0).remove(score.parts[0].flat[0])
score.parts[0].measure(0).insert(0, music21.clef.TrebleClef())

# Set the subtitle
score.metadata.movementName = "Vulfpeck"

# Let's use a jazzy font for the lyrics (Chords)
show(score,osmd_options={
        "defaultFontFamily": "Courier New",
        # make the lyrics a bit higher
        }, engraving_rules={
            "ChordSymbolTextHeight": 2.5,
            "ChordSymbolYOffset": 2
        })