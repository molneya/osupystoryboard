
from dataclasses import dataclass
import math, random

from pystoryboard.models import Storyboard
from pystoryboard.enums import Easing, Layer, Origin

@dataclass
class Drop:
    '''
    A drop for a rain storyboard effect.
    '''
    sb: Storyboard
    file_path: str
    fall_time: int

    def __post_init__(self) -> None:
        depth = random.uniform(0, 0.8)
        self.position = random.randint(-40, 680)

        # Drops with higher "depth" will be darker, smaller, and fall slower
        self.colour = int(255 - 255 * depth)
        self.scale = 1 - 0.2 * depth
        self.fall_time = int(self.fall_time + depth * 300)

    def generate(self, start: int, end: int) -> None:
        '''
        Generates a rain drop.
        '''
        loop_count = math.ceil((end - start) / self.fall_time)

        # Create a drop with a set colour and scale
        drop = self.sb.Sprite(Layer.Background, Origin.TopLeft, self.file_path, self.position)
        drop.Colour(self.colour, self.colour, self.colour).Scale(self.scale)

        # Create a loop for the drop to fall multiple times.
        # Note the usage of start and end here, since the above command lifetimes are calculated automatically.
        loop = drop.Loop(start, loop_count)
        loop.MoveY(-32, 480, 0, self.fall_time)

@dataclass
class Rain:
    '''
    A rain storyboard effect.
    '''
    sb: Storyboard
    file_path: str
    drop_count: int = 75
    fall_time: int = 500

    def generate(self, start: int, end: int) -> None:
        '''
        Generates rain.
        '''
        for _ in range(self.drop_count):
            # Generate drop
            drop = Drop(self.sb, self.file_path, self.fall_time)
            drop.generate(int(start), end)

            # Offset each drop to look more random
            start += self.fall_time / self.drop_count
