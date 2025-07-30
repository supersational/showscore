# showscore/converter/to_xml.py

from music21.musicxml.m21ToXml import GeneralObjectExporter

def from_music21(obj) -> str:
    """
    Converts a music21 object to a MusicXML string.

    Ensures that the object is a Score and that part names are not empty to
    prevent rendering issues in OSMD.

    :param obj: a music21 score or stream object.
    :return: MusicXML data as a UTF-8 encoded string.
    """
    gex = GeneralObjectExporter()
    # fromGeneralObject() ensures we are working with a Score object
    score = gex.fromGeneralObject(obj)

    try:
        # If a part has no name, OSMD may generate a long random string.
        # Giving it a single space is a cleaner workaround.
        for part in score.parts:
            if not part.partName:
                part.partName = " "
    except AttributeError:
        # This can happen if the object is an Opus, which doesn't have .parts
        pass

    # Generate the well-formed XML
    bytes_out = gex.parseWellformedObject(score)
    return bytes_out.decode("utf-8") 