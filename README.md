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

### How it looks

![Example code for rendering Bohemian Rhapsody](https://github.com/user-attachments/assets/a2501a11-5041-4755-999d-13e6f3edff6f)


### Other usage examples

We detect the environment automatically. If in a terminal the music will open in a new browser window.

```python
# tab=true makes it always open the score in new tab:
show(score, tab=True)
```

### Formatting options

Demo code for the below image is in [neon-fugue.py](neon-fugue.py) and some font stuff in [vulfpeck-demo.py](vulfpeck-demo.py).

<img width="1446" height="625" alt="image" src="https://github.com/user-attachments/assets/556d1d4e-548d-4471-94aa-62a92fc3d1a3" />


### Backend

Rendering using 'svg' (default) or 'canvas' will look the same, but have slight differences:
  - svg will (probably) look nicer when printing at high resolutions, and easier to modify.
  - canvas is faster to render and doesn't slow down scrolling.
  - use `showscore.show(score, backend='canvas')` to use canvas renderer

### Options

```yaml
score: The music21 score object to display.
title: A string to set as the score's title.
subtitle: A string to set as the score's subtitle.
composer: A string to set as the score's composer.
tab: If True, forces the score to open in a new browser tab.
osmd_options: A dictionary of top-level OSMD options (e.g., backend, darkMode).
engraving_rules: A dictionary of fine-grained OSMD EngravingRules.
```
See source code for more details on [osmd options](https://github.com/opensheetmusicdisplay/opensheetmusicdisplay/blob/c4209608320572c7875a21c99a5c263a14b45e17/src/OpenSheetMusicDisplay/OSMDOptions.ts#L21) and [engraving rules](https://github.com/opensheetmusicdisplay/opensheetmusicdisplay/blob/c4209608320572c7875a21c99a5c263a14b45e17/src/MusicalScore/Graphical/EngravingRules.ts#L26).

### Known bugs

Some corpus pieces give rendering errors. E.g. 'bach/bwv846' has an error in Chrome (but not VSCode). These are bugs in the underlying libraries - and error messages are displayed in red instead of the score.

- There is a known bug with displaying 'TempoExpressions' which is fixed in showscore 2.0.0 (since upgrading to OSMD 1.9.0).
- If you see anything else please open an [Issue](https://github.com/supersational/showscore/issues)

```python
from music21 import corpus
from showscore import show
score = corpus.parse('bach/bwv846')  # Prelude in C

show(score)
```

### Tested in

- VSCode Notebooks
- Jupyter lab
