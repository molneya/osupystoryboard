
from enum import Enum

class Layer(Enum):
    Background = 0
    Fail = 1
    Pass = 2
    Foreground = 3
    Overlay = 4

class Origin(Enum):
    TopLeft = 0
    Centre = 1
    CentreLeft = 2
    TopRight = 3
    BottomCentre = 4
    TopCentre = 5
    CentreRight = 7
    BottomLeft = 8
    BottomRight = 9

class Easing(Enum):
    Linear = 0
    EasingOut = 1
    EasingIn = 2
    QuadIn = 3
    QuadOut = 4
    QuadInOut = 5
    CubicIn = 6
    CubicOut = 7
    CubicInOut = 8
    QuartIn = 9
    QuartOut = 10
    QuartInOut = 11
    QuintIn = 12
    QuintOut = 13
    QuintInOut = 14
    SineIn = 15
    SineOut = 16
    SineInOut = 17
    ExpoIn = 18
    ExpoOut = 19
    ExpoInOut = 20
    CircIn = 21
    CircOut = 22
    CircInOut = 23
    ElasticIn = 24
    ElasticOut = 25
    ElasticHalfOut = 26
    ElasticQuarterOut = 27
    ElasticInOut = 28
    BackIn = 29
    BackOut = 30
    BackInOut = 31
    BounceIn = 32
    BounceOut = 33
    BounceInOut = 34

class LoopType(Enum):
    Forever = "LoopForever"
    Once = "LoopOnce"

class ParameterType(Enum):
    FlipHorizontal = "F"
    FlipVertical = "V"
    AdditiveBlending = "A"

class TriggerType(Enum):
    Passing = "Passing"
    Failing = "Failing"
