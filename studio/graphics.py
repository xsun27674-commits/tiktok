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


def text(c, x, y, value, size=11, color=LIGHT):
    face = font(size)
    width = int(face.getlength(value)) + 4
    glyphs = Image.new('1', (width, size+4))
    ImageDraw.Draw(glyphs).text((1,1),value,font=face,fill=1,anchor='lt')
    c.image.paste(color,(x,y,x+width,y+size+4),glyphs)


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


def label(c,x,y,value):
    width = round(font(10).getlength(value))+14
    c.bevel(x,y,width,17,INK,3)
    c.rect(x+5,y+4,2,9,GOLD)
    text(c,x+9,y+3,value,10)


def dialogue(c,value,*,x,y,w,tail=None,highlight=False):
    lines=wrap(value,w-24,12)
    if len(lines)>2:
        raise ValueError(f'Dialogue exceeds two lines: {value}')
    if tail is not None:
        c.poly([(x+6,y+14),(x+6,y+26),(tail,y+22)],GOLD)
    panel(c,x,y,w,43,accent=GOLD if highlight else '#c0996d')
    for i,line in enumerate(lines):
        text(c,x+10,y+(14 if len(lines)==1 else 6)+i*15,line,12)


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
