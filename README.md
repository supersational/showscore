# ShowScore

[Music21](https://github.com/cuthbertLab/music21) is an excellent library for
working with music notation in Python. However, to render sheet music you need
to install an external program and configure paths. ShowScore can render scores
beautifully, without any dependencies (and faster to boot!). We do this by using
[OpenSheetMusicDisplay](https://github.com/opensheetmusicdisplay/opensheetmusicdisplay),
an open-source music renderer written in JavaScript.

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

```python
from showscore import show
from music21 import corpus
score = corpus.parse('bwv565')

# score will be rendered below cell:
show(score)

# open score in new tab:
show(score, tab=True)
```

### Options

- `showscore.backend` - currently one of 'canvas' (default) or 'svg'
  - canvas is more performant and less laggy - but won't resize automatically
  - use `showscore.backend = 'svg'` to use svg renderer
- `show(score, title=True, tab=False)`
  - `title` - false to hide title
  - `tab` - open in new tab rather than inline

### Known bugs

Some corpus pieces give rendering errors. E.g. 'bach/bwv846' has an error in
Chrome. These are bugs in the OS If a piece fails to render it will display the
error message in red.

- Several pieces (e.g. 'bach/bwv846') will display 'Error rendering
  data:TypeError: Cannot read properties of undefined (reading
  'TempoExpressions')' this is a bug in OpenSheetMusicDisplay. For now use the
  fix below.
- If you see anything else open an [Issue

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
