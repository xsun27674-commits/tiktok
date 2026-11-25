"""Reusable stage blocking and shots for the studio's brand rituals."""
from PIL import Image
from art import Canvas, CREAM, GOLD, INK, LIGHT
from character import sprite
from studio.graphics import caption_text, font, subtitle
from studio.brand.archive import SLOTS, archive_card, book, cover, shelf

OPENING=4.6
PORTAL=1.0
RETURN=.85
ENDING=10.5
OPEN_LINE='今天，又发现了什么有趣的科学秘密呢？'
END_LINE='今天的知识，又发了一颗小芽。\n我们下次见！'


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
    if t<1.65:
        zoom(c,(160,20,320,110))
        pose(c,t,'confused','think',x=48,y=98)
        archive_card(c,caption,entry,120,29,scale)
        c.bevel(254,84,17,11,INK,2)
        c.rect(256,86,13,7,CREAM)
        c.line([(256,86),(262,90),(268,86)],'#a37751')
    else:
        pose(c,t,'happy','sprout',facing=-1)
        subtitle(caption,OPEN_LINE,scale)
    return finish(c,caption)


def end_card(size,t,scale):
    """A standalone brand card with the original sprout animation."""
    c=Canvas(size,'#263f34')
    caption=Canvas((size[0]*scale,size[1]*scale))
    pose(c,t,'happy','sprout',x=(size[0]-80)//2,y=29)
    slogan='让知识发芽'
    size_px=27
    x=(size[0]-font(size_px).getlength(slogan))/2
    caption_text(caption,x,114,slogan,size_px,scale,color=CREAM)
    return finish(c,caption)


def ending(room,t,records,collected,entry,scale):
    if t>=8.9:
        return end_card(room.size,t-8.9,scale)
    c,caption=canvas(room,scale)
    if t<3.1:
        zoom(c,(158,79,318,169))
        x,y=104,38
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
        pose(c,t,'happy','wave')
        subtitle(caption,END_LINE,scale)
    return finish(c,caption)
