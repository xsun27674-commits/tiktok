from dataclasses import dataclass
from fractions import Fraction
import math


@dataclass(frozen=True)
class BeatClock:
    bpm: int = 120

    def __post_init__(self):
        if self.bpm<=0:
            raise ValueError('BPM must be positive')

    def seconds(self, beat):
        return Fraction(60,self.bpm)*Fraction(beat)

    def beat(self, seconds):
        return seconds*self.bpm/60

    def pulse(self, seconds):
        beat=self.beat(seconds)
        return max(0, 1-(beat-math.floor(beat))*5)


@dataclass(frozen=True)
class Cue:
    beat: int
    dialogue: str
    expression: str = 'default'
    action: str = 'idle'
    visible: bool = True


@dataclass(frozen=True)
class Episode:
    title: str
    intro: tuple[Cue, ...]
    story: tuple[Cue, ...]
    summary: tuple[Cue, ...]
    story_start: int
    summary_start: int
    end: int
    story_scene: object
    paper: object = None
    paper_start: int | None = None
    farewell_start: int | None = None
    bpm: int = 120
