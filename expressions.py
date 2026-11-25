"""Reusable pixel glyphs and sprout poses, independent of the body action."""
from dataclasses import dataclass
import math

from art import BLUSH, GOLD, GREEN, LIGHT, LIME, MOSS


@dataclass(frozen=True)
class Expression:
    eyes: tuple[str, str]
    leaves: str
    mouth: str = ''
    blush: int = 0


EXPRESSIONS = {
    'default': Expression(('bar', 'bar'), 'sway'),
    'happy': Expression(('arch', 'arch'), 'sway', 'smile'),
    'excited': Expression(('spark', 'spark'), 'upright', 'smile', 1),
    'confused': Expression(('narrow', 'tall'), 'fold'),
    'surprised': Expression(('wide', 'wide'), 'upright'),
    'focused': Expression(('low', 'low'), 'upright'),
    'sad': Expression(('sad_left', 'sad_right'), 'droop', 'frown'),
    'scared': Expression(('small', 'small'), 'tremble', 'tense'),
    'smug': Expression(('arch', 'narrow'), 'sway', 'smirk'),
    'unamused': Expression(('narrow', 'narrow'), 'droop', 'flat'),
    'shy': Expression(('low', 'arch'), 'fold', '', 2),
    'sleepy': Expression(('closed', 'closed'), 'droop'),
    'dizzy': Expression(('spiral', 'spiral'), 'tremble'),
    'inspired': Expression(('spark', 'tall'), 'upright'),
    'laughing': Expression(('squeeze_left', 'squeeze_right'), 'sway', 'laugh', 1),
    'angry': Expression(('angry_left', 'angry_right'), 'upright', 'tense'),
}

# Each point is a whole pixel relative to the original eye or mouth anchor.
EYE_PATHS = {
    'arch': [(-2, 5), (0, 2), (2, 2), (4, 5)],
    'closed': [(-1, 3), (0, 5), (2, 5), (4, 3)],
    'sad_left': [(-2, 6), (1, 3), (3, 3)],
    'sad_right': [(-1, 3), (1, 3), (4, 6)],
    'squeeze_left': [(-2, 2), (3, 4), (-2, 6)],
    'squeeze_right': [(4, 2), (-1, 4), (4, 6)],
    'angry_left': [(-2, 1), (4, 4), (-1, 4)],
    'angry_right': [(4, 1), (-2, 4), (3, 4)],
    'spiral': [(1, 4), (2, 4), (2, 2), (-1, 2), (-1, 6), (4, 6), (4, 1)],
}
MOUTH_PATHS = {
    'smile': [(0, 0), (1, 1), (3, 1), (4, 0)],
    'smirk': [(0, 1), (2, 1), (4, 0)],
    'frown': [(0, 1), (1, 0), (3, 0), (4, 1)],
    'tense': [(0, 1), (1, 0), (2, 1), (3, 0), (4, 1)],
    'flat': [(0, 0), (4, 0)],
}


def draw_face(eyes, mouth, cheeks, h, name, blink=False):
    expression = EXPRESSIONS[name]
    for x, glyph in zip((38, 52), expression.eyes):
        y = h + 13
        if blink:
            eyes.rect(x-1, y+4, 4, 1, GOLD)
        elif glyph in EYE_PATHS:
            eyes.line([(x+dx, y+dy) for dx, dy in EYE_PATHS[glyph]], GOLD)
        elif glyph == 'spark':
            eyes.line([(x+1, y), (x+1, y+6)], GOLD)
            eyes.line([(x-2, y+3), (x+4, y+3)], GOLD)
            eyes.rect(x+1, y+3, 1, 1, LIGHT)
        else:
            dx, dy, width, height = {
                'bar': (0, 0, 3, 7), 'tall': (0, -1, 3, 9), 'wide': (-1, -2, 5, 9),
                'low': (0, 3, 3, 5), 'narrow': (-1, 4, 5, 2), 'small': (0, 2, 3, 3),
            }[glyph]
            eyes.bevel(x+dx, y+dy, width, height, GOLD, 1)
            eyes.rect(x+1, y+dy+1, 1, 1, LIGHT)
    for x in (33, 55):
        cheeks.bevel(x, h+22, 5, 2, BLUSH, 1)
        for offset in range(expression.blush):
            cheeks.rect(x+1+offset*2, h+21-offset, 1, 1, BLUSH)

    if expression.mouth == 'laugh':
        mouth.poly([(43,h+21),(49,h+21),(48,h+24),(45,h+24)], GOLD)
    elif expression.mouth:
        mouth.line([(44+dx, h+22+dy) for dx, dy in MOUTH_PATHS[expression.mouth]], GOLD)


def draw_sprout(canvas, head_y, mode, frame):
    """Move two outlined leaves around their stem joints using integer coordinates."""
    sway = round(2*math.sin(frame*math.tau/12))
    jitter = (0, 1, -1, 0)[frame%4]
    spread, rise, lean = {
        'sway': (0, 0, sway),
        'droop': (1, 7+abs(sway), 0),
        'upright': (-4, -1, sway//2),
        'tremble': (0, 2+jitter, jitter),
        'fold': (-7+abs(sway), 2, sway//2),
    }[mode]
    for side, outline, fill, vein in (
        (-1, [(0,0),(6,1),(12,-1),(16,-5),(16,-9),(12,-10),(6,-9),(1,-5)],
         [(1,-1),(8,-1),(13,-4),(15,-8),(10,-9),(5,-7)], [(2,-1),(7,-4),(12,-6)]),
        (1, [(0,0),(3,-6),(8,-10),(14,-10),(16,-8),(14,-3),(9,0)],
         [(2,-1),(5,-6),(9,-9),(14,-9),(14,-6),(10,-2)], [(2,-1),(6,-4),(10,-6)]),
    ):
        root = 40 if side < 0 else 41

        def points(vertices):
            return [
                (root + side*(x+round(spread*x/16))+round(lean*x/16),
                 max(0, head_y-8+y+round(rise*x/16)))
                for x,y in vertices
            ]

        canvas.line([(root,head_y+2),(root,head_y-5),points([(3,-2)])[0]],
                    MOSS, 2)
        canvas.poly(points(outline), MOSS)
        canvas.poly(points(fill), LIME if side < 0 else '#b8c16b')
        canvas.line(points(vein), GREEN)
