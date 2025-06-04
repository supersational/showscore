import os
import builtins
from unittest import mock
from showscore.html_renderer import showXML


def test_showxml_creates_temp_file(monkeypatch, tmp_path):
    xml = '<score-partwise></score-partwise>'

    fake_path = tmp_path / 'temp.html'
    monkeypatch.setattr('showscore.html_renderer.getTempFile', lambda suffix=None: str(fake_path))
    opened = {}
    def fake_open(path):
        opened['path'] = path
    monkeypatch.setattr('webbrowser.open_new_tab', fake_open)
    # ensure runningInNotebook returns False to avoid IPython call
    monkeypatch.setattr('showscore.html_renderer.runningInNotebook', lambda: False)

    showXML(xml, title=True, tab=False)

    assert opened['path'].startswith('file:///')
    assert fake_path.exists()
