import os
from showscore.utils import getTempFile, getUniqueDivId, runningInNotebook


def test_get_temp_file_suffix():
    path = getTempFile(suffix=".html")
    assert isinstance(path, str)
    assert path.endswith(".html")
    # file may or may not exist depending on platform; ensure directory exists
    assert os.path.isdir(os.path.dirname(path))


def test_unique_div_id_unique():
    id1 = getUniqueDivId()
    id2 = getUniqueDivId()
    assert id1 != id2
    assert id1.startswith("OSMD-")
    assert id2.startswith("OSMD-")
    assert "-" not in id1[5:]
    assert "-" not in id2[5:]


def test_running_in_notebook_false():
    assert runningInNotebook() is False
