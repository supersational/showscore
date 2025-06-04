import music21 as m21
from showscore.music21_converter import music21ScoreToXML


def make_simple_score():
    s = m21.stream.Score()
    p = m21.stream.Part()
    p.append(m21.note.Note('C4'))
    s.insert(0, p)
    return s


def test_music21_score_to_xml_contains_score_partwise():
    score = make_simple_score()
    xml = music21ScoreToXML(score)
    assert isinstance(xml, str)
    assert '<score-partwise' in xml
    assert '<part-list>' in xml
