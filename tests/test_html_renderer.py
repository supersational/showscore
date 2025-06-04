import webbrowser

from showscore import html_renderer
from showscore.html_renderer import musicXMLToScript, makeHTML, showXML


def test_musicxml_to_script_includes_options():
    xml = '<score-partwise></score-partwise>'
    div_id = 'abc123'
    script = musicXMLToScript(xml, div_id, showTitle=True)
    assert 'abc123' in script
    assert xml in script
    assert 'canvas' in script  # default backend


def test_make_html_contains_div_and_script():
    script = 'var x = 1;'
    html = makeHTML(script, 'div1', 'My Title')
    assert '<div id="div1"></div>' in html
    assert '<script>' in html
    assert 'My Title' in html


def test_showxml_inline(monkeypatch, tmp_path):
    """showXML should display inline when running in a notebook."""
    xml = '<score-partwise></score-partwise>'

    fake_path = tmp_path / 'temp.html'
    monkeypatch.setattr(html_renderer, 'getTempFile', lambda suffix=None: str(fake_path))
    monkeypatch.setattr(html_renderer, 'runningInNotebook', lambda: True)
    monkeypatch.setattr(webbrowser, 'open_new_tab', lambda url: None)

    import IPython
    if IPython.version_info[:2] >= (9, 0) and IPython.version_info[:2] != (9, 2):
        import IPython.core.display as cd
        if not hasattr(cd, 'display'):
            from IPython.display import display
            monkeypatch.setattr(cd, 'display', display, raising=False)

    showXML(xml, tab=False)
