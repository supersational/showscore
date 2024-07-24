def music21ScoreToXML(obj) -> str:
    """
    Prepare a score even if `obj` is not a Score, and ensure the part name is not empty.
    Return a string dump of the XML.

    :param obj: music21 score or general object
    :return: XML data as string
    """
    from music21.musicxml.m21ToXml import GeneralObjectExporter

    gex = GeneralObjectExporter()
    # whether or not obj is score, fromGeneralObject returns a score
    score = gex.fromGeneralObject(obj)

    try:
        # if the part name is empty OSMD will generate a long random string
        for part in score.parts:
            if not part.partName:
                part.partName = " "
    except:
        pass  # if it's an Opus for example, it doesn't have parts
    # run music21's converter
    bytesOut = gex.parseWellformedObject(score)
    return bytesOut.decode("utf-8")
