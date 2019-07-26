from pathlib import Path
from box import Box

rte = Box({}
    report_error = 'report_error',
})

mute = False

sounds_path = Path('sounds')
effects_path = sounds_path / 'effects'
music_path = sounds_path / 'music'