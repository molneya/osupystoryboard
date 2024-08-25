
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from .enums import Layer, Origin, Easing, LoopType, ParameterType, TriggerType

class Base:
    def _pack_enum(self, value: Enum) -> str:
        return f",{value.value}"

    def _pack_str(self, value: str) -> str:
        if ' ' in value:
            return f",\"{value}\""
        return f",{value}"

    def _pack_value(self, value: int | float) -> str:
        return f",{value:g}"

    def pack(self, object: str, default_start: int, default_end: int) -> str:
        for field in self.__dataclass_fields__:
            value = self.__dict__[field]

            # When the value is none, we have to use a default
            if value is None:
                if field == 'start':
                    object += self._pack_value(default_start)
                elif field == 'end':
                    object += self._pack_value(default_end)
                else:
                    raise ValueError(f"Unexpected field '{field}' was None")

            # Other values can be packed normally
            elif isinstance(value, Enum):
                object += self._pack_enum(value)
            elif isinstance(value, str):
                object += self._pack_str(value)
            else:
                object += self._pack_value(value)

        return object + '\n'

    def write(self, fp, level: int, default_start: int = 0, default_end: int = 0) -> None:
        packed = self.pack(' ' * level + self.name, default_start, default_end)
        fp.write(packed)

@dataclass
class BaseCommand(Base):
    '''
    Base for all storyboard commands.
    '''
    easing: Easing
    start: int
    end: int

@dataclass
class Fade(BaseCommand):
    start_opacity: float
    end_opacity: float

    def __post_init__(self) -> None:
        if self.end_opacity is None:
            self.end_opacity = self.start_opacity
        self.name = "F"

@dataclass
class Move(BaseCommand):
    start_x: float
    start_y: float
    end_x: float
    end_y: float

    def __post_init__(self) -> None:
        if self.end_x is None:
            self.end_x = self.start_x
        if self.end_y is None:
            self.end_y = self.start_y
        self.name = "M"

@dataclass
class MoveX(BaseCommand):
    start_x: float
    end_x: float

    def __post_init__(self) -> None:
        if self.end_x is None:
            self.end_x = self.start_x
        self.name = "MX"

@dataclass
class MoveY(BaseCommand):
    start_y: float
    end_y: float

    def __post_init__(self) -> None:
        if self.end_y is None:
            self.end_y = self.start_y
        self.name = "MY"

@dataclass
class Scale(BaseCommand):
    start_scale: float
    end_scale: float

    def __post_init__(self) -> None:
        if self.end_scale is None:
            self.end_scale = self.start_scale
        self.name = "S"

@dataclass
class VectorScale(BaseCommand):
    start_scale_x: float
    start_scale_y: float
    end_scale_x: float
    end_scale_y: float

    def __post_init__(self) -> None:
        if self.end_scale_x is None:
            self.end_scale_x = self.start_scale_x
        if self.end_scale_y is None:
            self.end_scale_y = self.start_scale_y
        self.name = "V"

@dataclass
class Rotate(BaseCommand):
    start_rotate: float
    end_rotate: float

    def __post_init__(self) -> None:
        if self.end_rotate is None:
            self.end_rotate = self.start_rotate
        self.name = "R"

@dataclass
class Colour(BaseCommand):
    start_red: int
    start_green: int
    start_blue: int
    end_red: int
    end_green: int
    end_blue: int

    def __post_init__(self) -> None:
        if self.end_red is None:
            self.end_red = self.start_red
        if self.end_green is None:
            self.end_green = self.start_green
        if self.end_blue is None:
            self.end_blue = self.start_blue
        self.name = "C"

@dataclass
class Parameter(BaseCommand):
    parameter: ParameterType

    def __post_init__(self) -> None:
        self.name = "P"

class BaseCompound(Base):
    '''
    Base for all compound commands and objects.
    '''
    def __post_init__(self) -> None:
        self.commands = []

    def _min_start(self) -> int:
        '''
        Gets the minimum start time of a command in this object.
        '''
        starts = [command.start for command in self.commands if command.start is not None]

        if len(starts) == 0:
            raise ValueError("A start value must be specified for atleast one command in this object")

        return min(starts)

    def _max_end(self) -> int:
        '''
        Gets the maximum end time of a command in this object.
        '''
        ends = [command.end for command in self.commands if command.end is not None]

        if len(ends) == 0:
            raise ValueError("An end value must be specified for atleast one command in this object")

        return max(ends)

    def Fade(
        self,
        start_opacity: float,
        end_opacity: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = Fade(easing, start, end, start_opacity, end_opacity)
        self.commands.append(command)
        return self

    def Move(
        self,
        start_x: float,
        start_y: float,
        end_x: float | None = None,
        end_y: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    )  -> Self:
        command = Move(easing, start, end, start_x, start_y, end_x, end_y)
        self.commands.append(command)
        return self

    def MoveX(
        self,
        start_x: float,
        end_x: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = MoveX(easing, start, end, start_x, end_x)
        self.commands.append(command)
        return self

    def MoveY(
        self,
        start_y: float,
        end_y: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = MoveY(easing, start, end, start_y, end_y)
        self.commands.append(command)
        return self

    def Scale(
        self,
        start_scale: float,
        end_scale: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = Scale(easing, start, end, start_scale, end_scale)
        self.commands.append(command)
        return self

    def VectorScale(
        self,
        start_scale_x: float,
        start_scale_y: float,
        end_scale_x: float | None = None,
        end_scale_y: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = VectorScale(easing, start, end, start_scale_x, start_scale_y, end_scale_x, end_scale_y)
        self.commands.append(command)
        return self

    def Rotate(
        self,
        start_rotate: float,
        end_rotate: float | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = Rotate(easing, start, end, start_rotate, end_rotate)
        self.commands.append(command)
        return self

    def Colour(
        self,
        start_red: int,
        start_green: int,
        start_blue: int,
        end_red: int | None = None,
        end_green: int | None = None,
        end_blue: int | None = None,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = Colour(easing, start, end, start_red, start_green, start_blue, end_red, end_green, end_blue)
        self.commands.append(command)
        return self

    def Parameter(
        self,
        parameter: ParameterType,
        start: int | None = None,
        end: int | None = None,
        easing: Easing = Easing.Linear,
    ) -> Self:
        command = Parameter(easing, start, end, parameter)
        self.commands.append(command)
        return self

    def write(self, fp, level: int = 0, default_start: int = 0, default_end: int = 0) -> None:
        # Write on commands level
        super().write(fp, level, default_start, default_end)

        # For commands without a specified start or end, use these defaults
        default_start = self._min_start()
        default_end = self._max_end()

        # Write on sub commands level
        for command in self.commands:
            command.write(fp, level + 1, default_start, default_end)

@dataclass
class Loop(BaseCompound):
    start: int
    count: int

    def __post_init__(self) -> None:
        super().__post_init__()
        self.name = "L"

    @property
    def end(self) -> int:
        '''
        The end time of the entire loop.
        '''
        return self.start + self.count * self._max_end()

@dataclass
class Trigger(BaseCompound):
    trigger: TriggerType
    start: int
    end: int

    def __post_init__(self) -> None:
        super().__post_init__()
        self.name = "T"

class BaseObject(BaseCompound):
    '''
    Base for all storyboard objects.
    '''
    def Loop(self, start: int, count: int) -> Loop:
        command = Loop(start, count)
        self.commands.append(command)
        return command

    def Trigger(self, start: int, end: int, trigger: TriggerType) -> Trigger:
        command = Trigger(trigger, start, end)
        self.commands.append(command)
        return command

@dataclass(init=False)
class Sprite(BaseObject):
    layer: Layer
    origin: Origin
    file_path: str
    x: int
    y: int

    def __init__(self, layer: Layer, origin: Origin, file_path: str, x: int = 0, y: int = 0):
        super().__post_init__()
        self.layer = layer
        self.origin = origin
        self.file_path = file_path
        self.x = x
        self.y = y
        self.name = "Sprite"

@dataclass(init=False)
class Animation(Sprite):
    frame_count: int
    frame_time: int
    loop: LoopType

    def __init__(self, layer: Layer, origin: Origin, file_path: str, frame_count: int, frame_time: int, loop: LoopType, x: int = 0, y: int = 0):
        super().__init__()
        super().__post_init__()
        self.frame_count = frame_count
        self.frame_time = frame_time
        self.loop = loop
        self.name = "Animation"

class Storyboard:
    def __init__(self, path):
        self.path = path
        self.objects = []

    def Sprite(
        self,
        layer: Layer,
        origin: Origin,
        file_path: str,
        x: int = 0,
        y: int = 0,
    ) -> Sprite:
        sprite = Sprite(layer, origin, file_path, x, y)
        self.objects.append(sprite)
        return sprite

    def Animation(
        self,
        layer: Layer,
        origin: Origin,
        file_path: str,
        frame_count: int,
        frame_time: int,
        loop: LoopType,
        x: int = 0,
        y: int = 0,
    ) -> Animation:
        animation = Animation(layer, origin, file_path, x, y, frame_count, frame_time, loop)
        self.objects.append(animation)
        return animation

    def compile(self) -> None:
        print(f"Compiling {len(self.objects)} storyboard objects...")
        with open(self.path, 'w') as f:
            self.write(f)

    def write(self, fp) -> None:
        fp.write("[Events]\n")
        fp.write("//Background and Video events\n")

        for layer in Layer:
            # Only write storyboard objects for this specific layer
            fp.write(f"//Storyboard Layer {layer.value} ({layer.name})\n")
            for object in filter(lambda x: x.layer == layer, self.objects):
                object.write(fp)

        fp.write("//Storyboard Sound Samples\n")
