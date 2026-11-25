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
    c.bevel(x,y,112,99,INK,4)
    c.bevel(x+2,y+1,108,93,'#5d8057',3)
    c.rect(x+7,y+5,2,84,'#8fa767')
    c.rect(x+13,y+9,90,1,'#b6c78a')
    c.rect(x+19,y+15,77,45,CREAM)
    caption_text(caption,x+29,y+21,entry.code,13,scale,color=INK)
    for i,line in enumerate(wrap(entry.theme,68,10)[:2]):
        caption_text(caption,x+22,y+37+i*10,line,10,scale,color=INK)
    if stamped:
        c.rect(x+14,y+66,86,20,'#c4d697')
        c.d.rectangle((x+15,y+67,x+98,y+84),outline='#345a46')
        caption_text(caption,x+19,y+72,'DISCOVERY COMPLETE',7,scale,color='#345a46')
