# ShowScore

[Music21](https://github.com/cuthbertLab/music21) is an excellent library for
working with music notation in Python. However, to render sheet music you need
to install an external program and configure paths. ShowScore can render scores
beautifully, without any dependencies (and faster to boot!). We do this by using
[OpenSheetMusicDisplay](https://github.com/opensheetmusicdisplay/opensheetmusicdisplay),
an open-source music renderer written in JavaScript.

### Install

`pip install showscore`

### Usage

```python
from music21 import *

# Your ABC notation as a string
abc_notation = "X:1\nT:My Tune\nM:4/4\nK:C\nCDEF|G2G2|A4|G2F2|E4|"

# Load the ABC notation from the string
score = converter.parse(abc_notation)

from showscore import show
show(score)
```

### Notebook example

![Example code for rendering Bohemian Rhapsody](https://github.com/user-attachments/assets/a2501a11-5041-4755-999d-13e6f3edff6f)


### Non-Jupyter usage

The music will open in a new browser window if run from a non-jupyter environment (e.g. interactive shell). Or can be specified manually:

```python
# open score in new tab:
show(score, tab=True)
```

### Options

- `showscore.backend` - currently one of 'canvas' (default) or 'svg'
  - canvas is faster to render and doesn't slow down scrolling
  - svg will (probably) look nicer when printing at high resolutions
  - use `showscore.backend = 'svg'` to use svg renderer
- `show(score, title=True, tab=False)`
  - `title` - false to hide title
  - `tab` - open in new tab rather than inline

### Known bugs

Some corpus pieces give rendering errors. E.g. 'bach/bwv846' has an error in Chrome (but not VSCode). These are bugs in the underlying libraries - and error messages are displayed in red instead of the score.

- There is a known bug with displaying 'TempoExpressions' which can be fixed with the below code.
- If you see anything else please open an [Issue](https://github.com/supersational/showscore/issues)

```python
from music21 import corpus
from showscore import show
score = corpus.parse('bach/bwv846')  # Prelude in C

# filter out metronome marks to fix rendering error
for el in score.recurse().getElementsByClass('MetronomeMark'):
    el.activeSite.remove(el)
    
show(score)
```

### Tested in

- VSCode Notebooks
- Jupyter lab
