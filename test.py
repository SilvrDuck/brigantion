from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.renderers import BarChart, SpeechBubble, Rainbow, Fire

print(FigletText("ROCKS!", font='big'))


f = lambda: 2
f1 = lambda: 12

print(Fire(10, 10, 'raustienrastui enrstuaie rstuaien', 0.5, 2, 3, bg=False))

import time
from tqdm import tqdm

for i in tqdm(range(12)):
    time.sleep(0.1)