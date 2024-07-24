import os
import json
import webbrowser
from .utils import getTempFile, runningInNotebook, getUniqueDivId

# currently at 1.8.8
SCRIPT_FILE = "opensheetmusicdisplay.min.js"
JS_PATH = os.path.join(os.path.dirname(__file__), "showscore.js")

# module defaults
backend = "canvas"


def musicXMLToScript(xml, divId, *, showTitle=True):
    """
    Converts the xml into Javascript which can be injected into a webpage to display the score.
    If divId is set then it will be used as the container, if not a new div will be created.

    :param xml: The musicXML to be rendered
    :param divId: The id of the div element to render the score in
    :param showTitle: Whether to show the title of the score
    """

    # javascript that loads library and replaces div contents with rendered score
    script = open(JS_PATH).read()

    # osmd options are passed directly to the OSMD constructor
    osmd_options = {
        "autoResize": True,
        "backend": backend,
        "drawTitle": showTitle,
    }
    script = script.replace("$$osmd_options", json.dumps(osmd_options))

    # since we can't link to files from a notebook (security risk) inject into file.
    with open(
        os.path.join(os.path.dirname(__file__), SCRIPT_FILE), "r", encoding="utf-8"
    ) as f:
        script_content = f.read()

    python_options = {
        "div_id": divId,
        "offline_script": script_content,
        "xml_data": xml,
    }

    script = script.replace("$$python_options", json.dumps(python_options, indent=1))

    return script


def makeHTML(script, divId, title):
    """
    Generate HTML to display the music score.

    :param script: Javascript to render the score
    :param divId: HTML div ID where the score will be rendered
    :param title: Title of the HTML page
    :return: HTML as string
    """
    return f"""
<html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
<div id="{divId}"></div>
<script>{script}</script>
</body>
    """.strip()


def showXML(xml, title=True, tab=False):
    """
    In Jupyter notebooks this will display the score inline.
    In non-notebook environments it will open a new browser tab.

    :param xml: The musicXML to be rendered
    :param title: Whether to show the title of the score
    :param tab: Force open in a new tab
    """
    divId = getUniqueDivId()

    script = musicXMLToScript(xml, divId, showTitle=title)

    if runningInNotebook() == True and tab == False:
        # display the score inline in the notebook
        from IPython.core.display import HTML, Javascript, display

        display(HTML(f'<div id="{divId}"></div>'))
        display(Javascript(script))
    else:
        # write a temporary file and open in a new browser tab
        tmpFile = getTempFile(suffix=".html")
        with open(tmpFile, "w", encoding="utf-8") as f:
            f.write(makeHTML(script, divId, ""))
        webbrowser.open_new_tab(f"file:///{str(tmpFile)}")
