"""Reusable stage blocking and shots for the studio's brand rituals."""
from PIL import Image
from art import Canvas, CREAM, GOLD, INK, LIGHT
from character import sprite, sprite_layers
from studio.graphics import caption_text, subtitle
from studio.brand.archive import SLOTS, archive_card, book, cover, shelf

OPENING=4.6
PORTAL=2.45
RETURN=.85
ENDING=10.5
OPEN_LINE='今天，又发现了什么有趣的科学秘密呢？'
END_LINE='今天的知识，又发了一颗小芽。\n我们下次见！'
SPROUT=(150,66)


def canvas(room,scale):
    c=Canvas(room.size)
    c.paste(room,0,0)
    return c,Canvas((room.width*scale,room.height*scale))


def finish(c,caption):
    image=c.image.resize(caption.image.size,Image.Resampling.NEAREST)
    image.alpha_composite(caption.image)
    return image


def zoom(c,box):
    c.image=c.image.crop(box).resize(c.image.size,Image.Resampling.NEAREST)
    from PIL import ImageDraw
    c.d=ImageDraw.Draw(c.image)


def pose(c,t,expression='default',action='idle',x=75,y=79,**kwargs):
    c.paste(sprite(action,int(t*(10 if action in ('wave','walk') else 6)),
                   expression=expression,emotion_frame=int(t*12),**kwargs),x,y)


def opening(room,t,entry,scale):
    c,caption=canvas(room,scale)
    if 1.05<=t<2.05:
        zoom(c,(160,20,320,110))
        pose(c,t,'confused','think',x=48,y=98)
        archive_card(c,caption,entry,120,29,scale)
        c.bevel(254,84,17,11,INK,2)
        c.rect(256,86,13,7,CREAM)
        c.line([(256,86),(262,90),(268,86)],'#a37751')
    else:
        pose(c,t,'happy' if t>=2.05 else 'default','sprout',facing=-1 if t>=2.05 else 1)
        if t>=2.05:
            subtitle(caption,OPEN_LINE,scale)
    if t<.65:
        shade=Image.new('RGBA',c.image.size,(35,32,56,round(205*(1-t/.65)**1.5)))
        c.image.alpha_composite(shade)
    return finish(c,caption)


def sprout_tap(room,t,scale):
    c,caption=canvas(room,scale)
    zoom(c,(40,40,200,130))
    layers=sprite_layers(expression='inspired' if t>=.78 else 'focused',
                         emotion_frame=int(t*10))
    head=Canvas((80,76))
    for name in ('body','arms','sprout','head','screen','eyes','mouth','blush'):
        head.paste(layers[name],0,0)
    image=head.image.resize((160,152),Image.Resampling.NEAREST)
    # A close-up shows the cuff peeking from behind the right edge of the head.
    if .22<=t<1.18:
        progress=max(0,1-abs(t-.78)/.56)
        x=round(196-26*progress)
        y=round(96-27*progress)
        elbow=(round(204-9*progress),101)
        path=[(207,119),elbow,(x+8,y+10)]
        c.line(path,INK,10)
        c.line(path,CREAM,6)
    c.paste(image,70,64)
    if .22<=t<1.18:
        c.bevel(x,y,12,14,INK,3)
        c.bevel(x+1,y+1,10,11,CREAM,2)
        c.rect(x+3,y+2,4,2,LIGHT)
    if .78<=t:
        radiance=max(0,1-(t-.78)/1.1)
        for i,(dx,dy) in enumerate(((-11,-2),(14,-11),(0,-15),(-20,-10),(21,0))):
            shift=round((1-radiance)*10)
            x=150+dx+(shift if dx>=0 else -shift)
            y=66+dy-shift
            c.rect(x,y,2+(i%2),2,GOLD if i%2 else '#c2e49a')
            if i%2:
                c.rect(x+1,y-2,1,6,'#e2efad')
    return finish(c,caption)


def ending(room,t,records,collected,entry,scale):
    c,caption=canvas(room,scale)
    if t<3.1:
        zoom(c,(158,79,318,169))
        x,y=104,38
        if t<.75:
            lift=round((.75-t)*28)
            for offset in (4,2,0):
                c.bevel(x+offset,y+lift+offset,110,76,INK,3)
                c.bevel(x+offset+1,y+lift+offset+1,108,74,LIGHT,3)
            for i in range(5):
                c.rect(x+14,y+lift+15+i*9,72-i%2*14,2,'#b4a281')
        else:
            cover(c,caption,entry,x,y,scale,t>=2.05)
        if 1.45<=t<2.55:
            drop=max(0,1-abs(t-2.05)/.6)
            sy=round(12+drop*78)
            c.bevel(145,sy,30,23,INK,3)
            c.bevel(148,sy+2,24,18,'#825b45',3)
            c.rect(147,sy+19,26,5,'#4c996a')
    elif t<5.1:
        shelf(c,collected if t>=4.45 else records)
        pos=min(len(collected),len(SLOTS))-1
        bx,by=SLOTS[pos]
        fraction=max(0,min(1,(t-3.45)))
        shift=round(31*(1-fraction))
        lift=round(12*(1-fraction))
        if t<4.45:
            book(c,bx+shift,by+lift,entry)
        zoom(c,(7,14,167,104))
        pose(c,t,'happy','idle',x=212,y=104,facing=-1)
    else:
        shelf(c,collected)
        pose(c,t,'happy','wave' if t<9.25 else 'sprout')
        if t<8.9:
            subtitle(caption,END_LINE,scale)
        else:
            caption_text(caption,109,28,'让知识发芽',20,scale,outline=True)
            for x,y in ((99,35),(219,33),(226,44)):
                c.rect(x-2,y,5,1,GOLD)
                c.rect(x,y-2,1,5,GOLD)
    return finish(c,caption)
