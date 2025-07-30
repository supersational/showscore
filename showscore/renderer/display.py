# showscore/renderer/display.py

import os
import json
import webbrowser
from ..utils import getTempFile, runningInNotebook, getUniqueDivId

SCRIPT_FILE = "opensheetmusicdisplay.1.9.0.min.js"
JS_PATH = os.path.join(os.path.dirname(__file__), "showscore.js")

def musicXMLToScript(xml: str, divId: str, *, osmd_options_override: dict = None) -> str:
    """
    Converts the xml into Javascript that can be injected into a webpage.

    :param xml: The MusicXML to be rendered.
    :param divId: The id of the div element to render the score in.
    :param osmd_options_override: A dictionary of OSMD options to override the defaults.
    :return: The complete JavaScript for rendering.
    """
    # Sensible defaults for OSMD. Users can override these.
    osmd_options = {
        "autoResize": True,
        "backend": "svg",  # SVG is more flexible and scalable than canvas
        # "drawTitle": True,
    }

    if osmd_options_override:
        osmd_options.update(osmd_options_override)

    # Load the JavaScript template
    script_template = open(JS_PATH).read()
    script_template = script_template.replace("$$osmd_options", json.dumps(osmd_options, indent=2))

    # Inject the OSMD library source code for offline use
    with open(os.path.join(os.path.dirname(__file__), SCRIPT_FILE), "r", encoding="utf-8") as f:
        osmd_library_content = f.read()

    # Prepare final options for injection into the script
    python_options = {
        "div_id": divId,
        "xml_data": xml,
        "offline_script": osmd_library_content,
    }
    final_script = script_template.replace("$$python_options", json.dumps(python_options))

    return final_script

def makeHTML(script: str, divId: str, title: str) -> str:
    """Generates a complete HTML page to display the music score."""
    return f"""
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>{title}</title>
</head>
<body>
    <div id=\"{divId}\"></div>
    <script>{script}</script>
</body>
</html>
    """.strip()

def render_xml(xml: str, *, tab: bool = False, osmd_options_override: dict = None):
    """
    Renders MusicXML in a Jupyter notebook or a new browser tab.

    :param xml: The MusicXML to be rendered.
    :param tab: If True, forces opening in a new browser tab.
    :param osmd_options_override: A dictionary of OSMD options.
    """
    divId = getUniqueDivId()
    script = musicXMLToScript(xml, divId, osmd_options_override=osmd_options_override)

    if runningInNotebook() and not tab:
        from IPython.core.display import HTML, Javascript, display
        display(HTML(f'<div id="{divId}" style="min-height: 200px;"></div>'))
        display(Javascript(script))
    else:
        tmpFile = getTempFile(suffix=".html")
        with open(tmpFile, "w", encoding="utf-8") as f:
            f.write(makeHTML(script, divId, "showscore"))
        webbrowser.open_new_tab(f"file:///{str(tmpFile)}") 