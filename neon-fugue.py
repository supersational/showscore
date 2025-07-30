from showscore import show
import music21 as m21

score = m21.corpus.parse('beethoven/opus133.mxl')
score = score.measures(0, 10)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)



part_colors = {
    "Neon Green": "#2BFA4A",
    "Vibrant Magenta": "#E0218A",
    "Electric Purple": "#942BFF",
    "Electric Blue": "#04D9FF",
}
idx_colors = {
    idx: col for idx, col in enumerate(part_colors.values())
}


for idx, part in enumerate(score.parts):
    print(idx, part.id, idx_colors[idx])
    part.color = idx_colors[idx]
    for n in part.recurse().getElementsByClass(m21.note.NotRest):
        if isinstance(n, m21.chord.Chord):
            for subnote in n.notes:
                subnote.style.color = idx_colors[idx]
        else:
            n.style.color = idx_colors[idx]

if 0:
    score = score.chordify()
    show(score, osmd_options={"darkMode": True, "drawTitle": False})
elif 0:
    from copy import deepcopy

    # 1. Start with a deepcopy of the first part as our base
    merged_part = deepcopy(score.parts[0])
    merged_part.id = 'MergedPart'

    # 2. Iterate through the REST of the parts and merge them in
    for part_to_merge in score.parts[1:]:
        merged_part.mergeElements(part_to_merge)

    # 3. Create a new score to display the single merged part
    merged_score = m21.stream.Score()
    merged_score.insert(0, merged_part)

    show(merged_score, osmd_options={"darkMode": True, "drawTitle": False})
else:
    show(score, osmd_options={"darkMode": True, "drawTitle": False}, engraving_rules={"DefaultColorMusic": "#CCCCCC"})








