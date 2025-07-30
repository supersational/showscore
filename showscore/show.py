# showscore/show.py

import music21
from .converter import from_music21
from .renderer import render_xml

def show(
    score: music21.stream.Score,
    *,
    backend: str = None,
    title: str = None,
    subtitle: str = None,
    composer: str = None,
    tab: bool = False,
    osmd_options: dict = None,
    engraving_rules: dict = None
):
    """
    Displays a music21 score in a notebook or browser using OpenSheetMusicDisplay.

    :param score: The music21 score object to display.
    :param title: A string to set as the score's title.
    :param subtitle: A string to set as the score's subtitle.
    :param composer: A string to set as the score's composer.
    :param tab: If True, forces the score to open in a new browser tab.
    :param osmd_options: A dictionary of top-level OSMD options (e.g., backend, darkMode).
    :param engraving_rules: A dictionary of fine-grained OSMD EngravingRules.
    """
    # 1. Ensure the score object has metadata
    if score.metadata is None:
        score.metadata = music21.metadata.Metadata()

    if isinstance(title, str):
        score.metadata.title = title

    if isinstance(subtitle, str):
        score.metadata.movementName = subtitle
    if isinstance(composer, str):
        score.metadata.composer = composer

    if score.metadata.title is None or score.metadata.title == "":
        osmd_options["drawTitle"] = False
    if score.metadata.movementName is None or score.metadata.movementName == "":
        osmd_options["drawSubtitle"] = False
    if score.metadata.composer is None or score.metadata.composer == "":
        osmd_options["drawComposer"] = False

    # 2. Convert the music21 object to a MusicXML string
    xml_data = from_music21(score)

    # 3. Prepare the rendering options
    final_osmd_options = osmd_options.copy() if osmd_options else {}
    if engraving_rules:
        # Nest the engraving rules within the main options object, as OSMD expects
        final_osmd_options["EngravingRules"] = engraving_rules

    if backend is not None:
        if backend not in ["canvas", "svg"]:
            raise ValueError(f"Invalid backend: {backend} (must be 'canvas' or 'svg')")
        final_osmd_options["backend"] = backend

    # 4. Render the MusicXML using the renderer module
    render_xml(xml_data, tab=tab, osmd_options_override=final_osmd_options) 