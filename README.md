# osu! py storyboard

Create osu! storyboards programmatically using python.

## Basic Usage

### Creating a Storyboard

To start, create a `Storyboard` which will be used to create other storyboard related objects.

```py
from pystoryboard.models import Storyboard

sb = Storyboard(r"path\to\storyboard.osb")
```

### Sprites and Animations

Create `Sprite`s and `Animation` objects using the `.Sprite` and `.Animation` methods respectively.

```py
from pystoryboard.enums import Layer, Origin, LoopType

my_sprite = sb.Sprite(
    Layer.Background,
    Origin.TopLeft,
    "sprite.png",
    x=200,
    y=300,
)

my_animation = sb.Animation(
    Layer.Background,
    Origin.Centre,
    "animation.png",
    x=100,
    y=100,
    frame_count=10,
    frame_time=33,
    loop=LoopType.Forever,
)
```

### Commands

Add commands to these objects using the familiar names.
Note that while these commands show the parameters in the original order, they are not implemented as such to allow for some shortcuts for ease of use, as seen in the advanced usage section.

```py
from pystoryboard.enums import Easing, ParameterType

my_sprite.Fade(
    easing=Easing.EasingIn,
    start=1000,
    end=2000,
    start_opacity=1.0,
    end_opacity=0.0,
)

my_sprite.Move(
    easing=Easing.QuadOut,
    start=1000,
    end=2000,
    start_x=0,
    start_y=0,
    end_x=640,
    end_y=480,
)

my_sprite.MoveX(
    easing=Easing.CubicInOut,
    start=1000,
    end=2000,
    start_x=0,
    end_x=640,
)

my_sprite.MoveY(
    easing=Easing.QuartIn,
    start=1000,
    end=2000,
    start_y=0,
    end_y=480,
)

my_sprite.Scale(
    easing=Easing.QuintOut,
    start=1000,
    end=2000,
    start_scale=0.5,
    end_scale=1.5,
)

my_sprite.VectorScale(
    easing=Easing.SineInOut,
    start=1000,
    end=2000,
    start_scale_x=2.0,
    start_scale_y=1.0,
    end_scale_x=0.5,
    end_scale_y=1.0,
)

my_sprite.Rotate(
    easing=Easing.ExpoIn,
    start=1000,
    end=2000,
    start_rotate=0.0,
    end_rotate=3.14,
)

my_sprite.Colour(
    easing=Easing.CircOut,
    start=1000,
    end=2000,
    start_red=255,
    start_green=255,
    start_blue=255,
    end_red=0,
    end_green=0,
    end_blue=0,
)

my_sprite.Parameter(
    easing=Easing.ElasticHalfOut,
    start=1000,
    end=2000,
    parameter=ParameterType.FlipHorizontal,
)
```

### Loops and Triggers

To make `Loops` and `Triggers`, start by making a loop or trigger object, then use commands like you would for a `Sprite` or `Animation`, with the limitation you can't nest `Loop`s or `Trigger`s.
Remember that these command starts and ends are relative to the parent's start time.

```py
from pystoryboard.enums import Easing, TriggerType

my_sprite_loop = my_sprite.Loop(start=3000, count=5)
my_sprite_loop.MoveX(easing=Easing.BackInOut, start=0, end=1000, start_x=640, end_x=0)

my_sprite_trigger = my_sprite.Loop(start=3000, end=6000, trigger=TriggerType.Failing)
my_sprite_trigger.MoveY(easing=Easing.BackInOut, start=0, end=1000, start_y=480 end_y=0)
```

### Compiling and viewing

Finally, compile the storyboard.

```py
sb.compile()
```

To view the new storyboard, run the script and `CTRL+L` in the osu! editor to reload the storyboard file.

## Advanced Usage

### Sprite/Animation shortcuts

When creating a `Sprite` or `Animation`, it's not actually required to specify the `x` or `y` parameter, since it's a fairly common pattern to move it right after creation.
In this case, it will default to `x=0`, `y=0`.

```py
from pystoryboard.enums import Layer, Origin, LoopType

my_sprite = sb.Sprite(Layer.Background, Origin.TopLeft, "sprite.png")
my_animation = sb.Animation(Layer.Background, Origin.Centre, "animation.png", 10, 33, LoopType.Forever)
```

### Command shortcuts

When adding commands, most arguments don't actually need to be specified to work. To accomodate this, the parameter order is rearranged.

| Original             | pystoryboard         |
| -------------------- | -------------------- |
| easing               | start/end parameters |
| start/end time       | start/end time       |
| start/end parameters | easing               |

The only required argument for every command is the start parameter. For `Loop`s and `Trigger`s, all parameters are still required.

In general, the rules for commands are:
- If no end parameter is specified, the object will use the start parameters for the end parameters.
- If no start time is specified, the start time will be the earliest start time of any other command in the object.
- If no end time is specified, the end time will be the latest end time of any other command in the object.
- If no easing is specified, it will default to `Easing.Linear`.
- Atleast one start time and end time is required per object (which can be in a loop).

Here is an example:

```py
# Scales to 0.5 and colours grey for the lifetime of the object.
my_sprite.Scale(0.5).Colour(128, 128, 128)

# Moves sprite from x=0 to x=640 in 500ms, starting from t=1000, looping 10 times.
# This fulfils the rules on specifying start and end times, since the start time is defined
# by the `Loop` start and `MoveX` start, and the end is defined from the `MoveX` end.
my_sprite_loop = my_sprite.Loop(1000, 10)
    my_sprite_loop.MoveX(0, 640, 0, 500)
```

When compiled, this will populate the start time and end time for the `Scale` and `Colour` command automatically, so you don't have to worry about manually calculating it.

## Effects

On their own, while (probably) more useful and readable than their notepad versions, commands can't do much.
Instead, to create something more visually appealing, pre-defined sets of commands can be used to make something bigger.

More to be added later.

### Rain

An effect where particles fall from the top of the screen.

```py
from effects.rain import Rain

rain = Rain(sb, "rain.png", drop_count=75, fall_time=500)
rain.generate(7705, 16160) # effect ranges from 00:07:705 to 00:16:160
```
