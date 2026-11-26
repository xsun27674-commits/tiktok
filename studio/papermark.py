"""PaperMark evidence overlays. Images come only from local, sourced originals."""
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from subprocess import check_output
from urllib.parse import urlsplit

from PIL import Image, ImageDraw, ImageOps
from art import Canvas, GOLD, INK, LIGHT
from studio.graphics import caption_text, panel, subtitle, wrap

INTRO_SECONDS = 13
REFLECTION_SECONDS = 12
W, H = 320, 180


def required(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'PaperMark requires {name}')
    return value


def url(value):
    if urlsplit(value).scheme != 'https' or not urlsplit(value).hostname:
        raise ValueError('Source and rights URLs must use HTTPS')
    return value


def source_image(root, spec):
    url(spec['source_url'])
    url(spec['rights_url'])
    required(spec['rights_note'], 'a reuse-rights or permission record')
    if spec.get('allow_reproduction') is not True:
        raise ValueError('Source reproduction permission has not been established')
    path=(root/spec['file']).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Source paths must stay inside the manifest folder')
    data=path.read_bytes()
    if sha256(data).hexdigest()!=spec['sha256']:
        raise ValueError(f'Source checksum mismatch: {path.name}')
    kind=spec['kind']
    if kind=='pdf_first_page':
        if not data.startswith(b'%PDF-'):
            raise ValueError('Expected the original paper PDF')
        data=check_output(['pdftoppm','-f','1','-l','1','-r','110','-png'],input=data)
    elif kind not in ('publisher_capture','original_figure'):
        raise ValueError(f'Unsupported source type: {kind}')
    with Image.open(BytesIO(data)) as image:
        return image.convert('RGB')


@dataclass
class Figure:
    start: float
    end: float
    number: str
    citation: str
    image: Image.Image

    def overlay(self, frame, scale):
        palette=Canvas((W,H),'#293b34')
        letters=Canvas((W*scale,H*scale))
        # Preserve the source aspect ratio and the lower host area.
        panel(palette,15,3,288,115,'#809c72')
        caption_text(letters,23,9,self.number,10,scale,color=GOLD)
        image=ImageOps.contain(self.image,(266*scale,84*scale),Image.Resampling.LANCZOS)
        frame.paste(palette.image.resize(frame.size,Image.Resampling.NEAREST).crop(
            (0,0,W*scale,124*scale)),(0,0))
        frame.paste(image,((W*scale-image.width)//2,22*scale))
        caption_text(letters,23,108,self.citation,8,scale)
        frame.alpha_composite(letters.image)
        return frame


class PaperMark:
    def __init__(self, manifest):
        path=Path(manifest).resolve()
        spec=json.loads(path.read_text(encoding='utf-8'))
        self.info={key:required(spec[key],key) for key in (
            'title_en','title_zh','authors','institutions','journal',
            'publication_date','doi','limitations','open_questions')}
        date.fromisoformat(self.info['publication_date'])
        url(f"https://doi.org/{self.info['doi']}")
        front=spec['front_page']
        if front['kind'] not in ('pdf_first_page','publisher_capture'):
            raise ValueError('Use an original PDF first page or journal page capture as the cover')
        self.page=source_image(path.parent,front)
        self.highlights=[]
        for row in spec['highlights']:
            box=tuple(row['box'])
            if len(box)!=4 or not (0<=box[0]<box[2]<=1 and 0<=box[1]<box[3]<=1):
                raise ValueError('Highlights require a normalized x0, y0, x1, y1 box')
            self.highlights.append((box,required(row['keyword'],'highlight keyword')))
        if not self.highlights:
            raise ValueError('At least one sourced reading highlight is required')
        self.figures=[]
        for item in spec.get('figures',[]):
            if item['kind']!='original_figure':
                raise ValueError('Figure inserts must use a sourced original figure')
            start,end=float(item['start']),float(item['end'])
            number=required(item['figure'],'figure number')
            if not number.startswith('Figure ') or not (0<=start<end):
                raise ValueError('Use a Figure label and increasing story-local seconds')
            citation=required(item['citation'],'on-screen figure credit')
            if len(wrap(citation,268,8))>1:
                raise ValueError('Use a compact on-screen figure credit, e.g. authors, year, DOI')
            self.figures.append(Figure(start,end,number,citation,source_image(path.parent,item)))
        self.figures.sort(key=lambda f:f.start)
        if any(a.end>b.start for a,b in zip(self.figures,self.figures[1:])):
            raise ValueError('Figure inserts must not overlap')

    def intro(self, room, t, code, scale):
        size=(W*scale,H*scale)
        if t<1.35:
            fraction=t/1.35
            fraction=fraction*fraction*(3-2*fraction)
            bounds=tuple(round(a+(b-a)*fraction) for a,b in zip((0,0,W,H),(233,46,320,95)))
            return room.crop(bounds).resize(size,Image.Resampling.NEAREST)
        if t>=6.5:
            return self.card(code,scale)
        scene=Canvas((W,H),'#263a32')
        panel(scene,11,8,296,162,'#92aa76')
        frame=scene.image.resize(size,Image.Resampling.NEAREST)
        letters=Canvas(size)
        image=ImageOps.contain(self.page,(137*scale,151*scale),Image.Resampling.LANCZOS)
        left,top=23*scale, 14*scale
        frame.paste(image,(left,top))
        current=min(len(self.highlights)-1,int((t-1.35)/5.15*len(self.highlights)))
        box,keyword=self.highlights[current]
        crop=tuple(round(v*n) for v,n in zip(box,(*self.page.size,*self.page.size)))
        if crop[0]>=crop[2] or crop[1]>=crop[3]:
            raise ValueError('Highlight is smaller than a source pixel')
        overlay=(left+round(box[0]*image.width),top+round(box[1]*image.height),
                 left+round(box[2]*image.width),top+round(box[3]*image.height))
        draw=ImageDraw.Draw(frame)
        draw.rectangle(overlay,outline=GOLD,width=scale)
        # A stepped lens drifts into place when a new reading target appears.
        step=(t-1.35)*len(self.highlights)/5.15
        slide=round(5*max(0,1-(step%1)*5))
        lx=round((overlay[2]+overlay[0])/2)
        ly=overlay[3]+slide*scale
        draw.line([(lx+4*scale,ly+4*scale),(lx+10*scale,ly+10*scale)],fill=GOLD,width=2*scale)
        draw.ellipse((lx-6*scale,ly-6*scale,lx+6*scale,ly+6*scale),outline=GOLD,width=scale)
        detail=ImageOps.contain(self.page.crop(crop),(127*scale,62*scale),Image.Resampling.LANCZOS)
        frame.paste(detail,(168*scale,49*scale))
        caption_text(letters,167,27,'研究原文 · 阅读焦点',11,scale,color=GOLD)
        for i,line in enumerate(wrap(keyword,128,11)):
            if i>=3:
                raise ValueError('Reading keyword exceeds the safe area')
            caption_text(letters,169,115+i*13,line,11,scale)
        frame.alpha_composite(letters.image)
        return frame

    def card(self, code, scale):
        base=Canvas((W,H),'#25382f')
        panel(base,13,10,292,157,'#9ab278')
        surface=Canvas((W*scale,H*scale))
        caption_text(surface,26,19,f'PaperMark  ·  {code}',12,scale,color=GOLD)
        y=40
        for field,label,size in (('title_en','',10),('title_zh','',11),
                                 ('authors','作者  ',9),('institutions','机构  ',9),
                                 ('journal','期刊  ',9),('publication_date','发表  ',9),
                                 ('doi','DOI  ',8)):
            for line in wrap(label+self.info[field],266,size):
                if y+size>157:
                    raise ValueError('PaperMark information card is too dense; provide a brief credited author/institution display list')
                caption_text(surface,26,y,line,size,scale)
                y+=size+2
            y+=1
        result=base.image.resize(surface.image.size,Image.Resampling.NEAREST)
        result.alpha_composite(surface.image)
        return result

    def reflect(self, room, seconds, scale):
        from character import sprite

        base=Canvas((W,H))
        base.paste(room,0,0)
        base.paste(sprite('think',int(seconds*5),expression='focused'),75,79)
        overlay=Canvas((W*scale,H*scale))
        limitation=seconds<REFLECTION_SECONDS/2
        caption_text(overlay,16,13,'研究局限' if limitation else '还没解答的问题',12,
                     scale,outline=True,color=GOLD)
        subtitle(overlay,self.info['limitations' if limitation else 'open_questions'],scale)
        frame=base.image.resize(overlay.image.size,Image.Resampling.NEAREST)
        frame.alpha_composite(overlay.image)
        return frame
