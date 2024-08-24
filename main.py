
from pystoryboard.models import Storyboard
from effects.rain import Rain

sb = Storyboard(r"E:\osu!\Songs\beatmap-638599836218983758-audio\TrySail - adrenaline!!! (molneya).osb")

rain = Rain(sb, "rain.png", drop_count=75, fall_time=500)
rain.generate(7705, 16160)

sb.compile()
