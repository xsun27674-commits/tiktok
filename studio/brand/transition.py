"""The sprout glow and particle-led reveal."""
import math
import random

from PIL import Image
from art import Canvas

GREEN_STEPS=('#3c6859','#598c60','#87ad63','#bdd480','#e6ebaf')
RNG=random.Random(199)
SPECKS=tuple((RNG.uniform(0,math.tau),RNG.uniform(.4,1),RNG.randrange(5))
             for _ in range(64))


def reveal(source,dest,t,origin,scale):
    """A staggered tile reveal follows the outward-moving sprout particles."""
    w,h=source.size
    result=source.copy()
    x0,y0=origin
    if t>=1:
        return dest.copy()
    for y in range(0,h//scale,8):
        for x in range(0,w//scale,8):
            beat=math.hypot(x+4-x0,y+4-y0)/245+(x*13+y*7)%11*.009
            if beat<t*1.46:
                box=(x*scale,y*scale,min(w,(x+8)*scale),min(h,(y+8)*scale))
                result.paste(dest.crop(box),box[:2])
    glow=Canvas((w//scale,h//scale))
    for angle,speed,color in SPECKS:
        distance=t*250*speed
        x=round(x0+math.cos(angle)*distance)
        y=round(y0+math.sin(angle)*distance*.64)
        size=2 if color%2 else 3
        if (color+1)/5>t-.12 and t>0:
            glow.rect(x,y,size,size,GREEN_STEPS[color])
            if color==4:
                glow.rect(x-1,y+1,size+2,1,GREEN_STEPS[3])
    result.alpha_composite(glow.image.resize((w,h),Image.Resampling.NEAREST))
    return result
