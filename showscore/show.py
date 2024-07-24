from .music21_converter import music21ScoreToXML
from .html_renderer import showXML


def show(score, title=True, tab=False):
    """
    Show a score in a notebook or browser.
    :param score: a music21 score
    :param title: False to hide the title (default True)
    """
    score_type = str(type(score))
    score_type = score.__class__.__module__

    if score_type.startswith("music21."):
        xml = music21ScoreToXML(score)
    else:
        raise ValueError(f"Unknown score type: {score_type}")

    if "<movement-title>Music21 Fragment</movement-title>" in xml:
        title = False
    showXML(xml, title=title, tab=tab)
