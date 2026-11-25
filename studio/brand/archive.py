"""Persistent episode catalog and its reusable archive-book and shelf artwork."""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from art import CREAM, GOLD, INK, LIGHT
from studio.graphics import caption_text, panel, wrap

PALETTE=('#769454','#568579','#bc824e','#a36655','#9c9452')
SLOTS=((63,47),(63,69),(63,91),
       *((x,y) for y in (47,69,91) for x in range(25,62,7)))


@dataclass(frozen=True)
class Archive:
    number: int
    theme: str
    doi: str = ''

    def __post_init__(self):
        if type(self.number) is not int or self.number<1 or not self.theme.strip():
            raise ValueError('Archive requires a positive episode number and theme')

    @property
    def code(self):
        return f'SA-{self.number:03d}'


def load(path):
    path=Path(path)
    records=tuple(Archive(**row) for row in json.loads(path.read_text(encoding='utf-8'))) if path.exists() else ()
    if len({row.number for row in records})!=len(records):
        raise ValueError('Duplicate archive numbers in catalog')
    return tuple(sorted(records,key=lambda row:row.number))


def collect(records,entry):
    prior=next((row for row in records if row.number==entry.number),None)
    if prior and prior!=entry:
        raise ValueError(f'{entry.code} already belongs to {prior.theme}')
    return tuple(sorted(records if prior else (*records,entry),key=lambda row:row.number))


def save(path,entry):
    path=Path(path)
    records=collect(load(path),entry)
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps([asdict(row) for row in records],ensure_ascii=False,indent=2)+'\n',
                         encoding='utf-8')
    temporary.replace(path)


def shelf(c,records):
    """Fill shelves left to right with the most recent files; the catalog keeps all."""
    for i,entry in enumerate(records[-len(SLOTS):]):
        x,y=SLOTS[i]
        book(c,x,y,entry)


def book(c,x,bottom,entry):
    color=PALETTE[(entry.number-1)%len(PALETTE)]
    c.bevel(x-1,bottom-15,8,15,INK,1)
    c.rect(x,bottom-14,6,13,color)
    c.rect(x+1,bottom-13,4,1,CREAM)
    c.rect(x+1,bottom-10,4,3,GOLD)
    c.rect(x+1,bottom-4,4,1,INK)


def archive_card(c,caption,entry,x,y,scale):
    panel(c,x,y,135,53,'#8cb06e')
    caption_text(caption,x+10,y+7,f'科学档案  {entry.code}',10,scale)
    for i,line in enumerate(wrap(entry.theme,115,13)[:2]):
        caption_text(caption,x+10,y+23+i*14,line,13,scale)


def cover(c,caption,entry,x,y,scale,stamped):
    # A stepped page block sits behind the cloth front cover.
    c.bevel(x+3,y+4,115,99,INK,5)
    c.bevel(x+5,y+7,111,94,'#e5c79a',4)
    for yline in (93,96,99):
        c.rect(x+12,y+yline,97,1,'#a78465')
    for xline in (109,112):
        c.rect(x+xline,y+19,1,71,'#a78465')
    c.bevel(x,y,110,93,INK,5)
    c.bevel(x+2,y+1,106,89,'#526f4b',4)
    c.rect(x+3,y+7,10,77,'#344e3a')
    c.rect(x+12,y+4,2,83,'#91a263')
    c.rect(x+15,y+6,88,1,'#829760')
    c.rect(x+18,y+86,83,1,'#3e5941')
    for corner_x in (x+4,x+96):
        for corner_y in (y+6,y+78):
            c.rect(corner_x,corner_y,8,2,'#899c60')
            c.rect(corner_x,corner_y+2,2,5,'#758c58')
    for i in range(39):
        px=17+(i*37)%87
        py=9+(i*23)%74
        c.rect(x+px,y+py,2,1,'#607c52' if i%3 else '#496347')
    c.rect(x+26,y+16,71,40,INK)
    c.bevel(x+27,y+17,69,38,'#ead4a6',2)
    c.rect(x+31,y+20,59,1,'#f6e4b8')
    c.rect(x+31,y+51,59,1,'#c0a478')
    # Keep the compact label legible at playback size.
    def ink(px,py,value,size,color):
        caption_text(caption,x+px,y+py,value,size,scale,color=color)

    ink(34,24,entry.code,12,INK)
    for i,line in enumerate(wrap(entry.theme,59,8)[:2]):
        ink(31,37+i*9,line,8,INK)
    for bx,by in ((23,20),(98,21),(23,49),(98,50)):
        c.rect(x+bx,y+by,2,2,'#bea36b')

    if stamped:
        c.bevel(x+17,y+62,84,20,'#aec581',2)
        for dx in (0,20,41,62):
            c.rect(x+21+dx,y+64,15,1,'#496d46')
            c.rect(x+21+dx,y+79,14,1,'#496d46')
        for i in range(8):
            c.rect(x+19+(i*31)%80,y+63+(i*7)%17,1,1,'#769658')
        ink(22,69,'DISCOVERY COMPLETE',7,'#2e523b')
