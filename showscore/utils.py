import importlib.util
import sys
import tempfile
import uuid


def getTempFile(suffix=None):
    file = tempfile.NamedTemporaryFile(suffix=suffix)
    return file.name


def getUniqueDivId() -> str:
    """
    Generate a unique ID for a HTML element

    :return: Unique ID as string
    """
    return "OSMD-" + str(uuid.uuid4()).replace("-", "")


def runningInNotebook() -> bool:
    """
    return bool if we are running under Jupyter Notebook (not IPython terminal)
    or Google Colabatory (colab).

    Methods based on:

    https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    """
    if sys.stderr.__class__.__name__ == "OutStream":
        return True
    else:
        return False
