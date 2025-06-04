import importlib
import music21 as m21
from showscore import show
show_module = importlib.import_module('showscore.show')


def make_simple_score():
    s = m21.stream.Score()
    p = m21.stream.Part()
    p.append(m21.note.Note('C4'))
    s.insert(0, p)
    return s


def test_show_invokes_showxml(monkeypatch):
    score = make_simple_score()
    called = {}

    def fake_showxml(xml, title=True, tab=False):
        called['xml'] = xml
        called['title'] = title
        called['tab'] = tab

    monkeypatch.setattr(show_module, 'showXML', fake_showxml)
    show(score)
    assert 'xml' in called
    assert '<score-partwise' in called['xml']


def test_show_raises_for_unknown_type():
    class Dummy: pass
    dummy = Dummy()
    try:
        show(dummy)
    except ValueError as e:
        assert 'Unknown score type' in str(e)
    else:
        assert False, 'ValueError not raised'
