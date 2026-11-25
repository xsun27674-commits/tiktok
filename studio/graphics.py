"""Brand typography, dialogue, research cards, and shot transitions."""
from dataclasses import dataclass
from functools import lru_cache
import os

from PIL import ImageFont, ImageDraw, Image
from art import Canvas, CREAM, GOLD, INK, LIGHT, MOSS

PANEL = '#45352d'
TEAL = '#577768'
DEFAULT_FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
WIDTH, HEIGHT = 320, 180


@lru_cache
def font(size):
    path = os.environ.get('STUDIO_CJK_FONT', DEFAULT_FONT)
    index = int(os.environ.get('STUDIO_CJK_FONT_INDEX', '2'))
    return ImageFont.truetype(path, size, index=index)


@lru_cache(maxsize=256)
def glyph_mask(value, size):
    width = int(font(size).getlength(value)) + 4
    glyphs = Image.new('L', (width*2, (size+4)*2))
    ImageDraw.Draw(glyphs).text((2,2),value,font=font(size*2),fill=255,anchor='lt')
    return glyphs.resize((width,size+4), Image.Resampling.LANCZOS)


def text(c, x, y, value, size=11, color=LIGHT):
    mask = glyph_mask(value, size)
    c.image.paste(color,(x,y,x+mask.width,y+mask.height),mask)


def subtitle(c, value):
    lines = wrap(value.replace('\n', ' '), WIDTH-30, 12)
    if len(lines)>2:
        raise ValueError(f'Subtitle exceeds two lines: {value}')
    for row, line in enumerate(lines):
        mask = glyph_mask(line, 12)
        x = (WIDTH-mask.width)//2
        y = 163-(len(lines)-1-row)*14
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(0,2)):
            text(c,x+dx,y+dy,line,12,INK)
        text(c,x,y,line,12)


def wrap(value, limit, size):
    current = ''
    lines = []
    for token in value.splitlines():
        for char in token:
            if current and font(size).getlength(current+char)>limit and char not in '，。？！、；）':
                lines.append(current.rstrip())
                current = ''
            current += char if current or char != ' ' else ''
        if current:
            lines.append(current.rstrip())
        current = ''
    return lines


def panel(c,x,y,w,h,accent=GOLD):
    c.bevel(x+2,y+2,w,h,INK,4)
    c.bevel(x,y,w,h,accent,4)
    c.bevel(x+1,y+1,w-2,h-2,PANEL,3)


def dialogue(c,value,*,x,y,w,tail=None,highlight=False):
    lines=wrap(value,w-20,11)
    if len(lines)>2:
        raise ValueError(f'Dialogue exceeds two lines: {value}')
    height=32 if len(lines)==2 else 23
    if tail is not None:
        c.poly([(x+6,y+8),(x+6,y+17),(tail,y+14)],GOLD)
    panel(c,x,y,w,height,accent=GOLD if highlight else '#c0996d')
    for i,line in enumerate(lines):
        text(c,x+9,y+4+i*13,line,11)


@dataclass(frozen=True)
class Paper:
    title: str
    authors: str
    journal: str
    year: int
    doi: str


def paper_card(paper):
    c=Canvas((WIDTH,HEIGHT))
    c.rect(0,0,WIDTH,HEIGHT,'#342c28')
    panel(c,15,13,288,150,TEAL)
    text(c,29,24,'论文信息',12,GOLD)
    c.rect(29,41,260,1,'#907350')
    cursor=47
    for value,size,color in (
        (paper.title,12,LIGHT),(f'作者  {paper.authors}',10,CREAM),
        (f'期刊  {paper.journal}  ·  {paper.year}',10,CREAM),(f'DOI  {paper.doi}',10,GOLD),
    ):
        for line in wrap(value,252,size):
            if cursor+size>153:
                raise ValueError('Paper card exceeds the safe area')
            text(c,29,cursor,line,size,color)
            cursor+=size+3
        cursor+=4
    return c.image


def curtain(c,progress):
    """An opaque stepped wipe at the cut, swept in and then out."""
    coverage=1-abs(progress*2-1)
    if coverage<=0:
        return
    for y in range(0,HEIGHT,10):
        offset=(y//10%5)*5
        edge=max(0,min(WIDTH,round(coverage*(WIDTH+20))-offset))
        if not edge:
            continue
        if progress<=.5:
            c.rect(0,y,edge,10,MOSS)
            if edge<WIDTH:
                c.rect(max(0,edge-3),y,min(edge,3),10,GOLD)
        else:
            c.rect(WIDTH-edge,y,edge,10,MOSS)
            if edge<WIDTH:
                c.rect(WIDTH-edge,y,min(edge,3),10,GOLD)
