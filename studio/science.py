"""Small building blocks for sourced science figures in the story safe area."""
from dataclasses import dataclass
import math

from art import GOLD, LIGHT, MOSS
from studio.graphics import caption_text


@dataclass(frozen=True)
class Source:
    citation: str
    locator: str  # DOI/URL and figure, table, or supplement identifier.

    def __post_init__(self):
        if not self.citation.strip() or not self.locator.strip():
            raise ValueError('Science figures require a citation and precise source locator')


def diagram(canvas, nodes, links, *, active=None):
    """Draw a protocol or mechanism as movable nodes and directed connections.

    Nodes are (x, y) coordinates. Add labels on the story caption layer.
    """
    for start,end in links:
        a,b=nodes[start],nodes[end]
        angle=math.atan2(b[1]-a[1],b[0]-a[0])
        tip=(round(b[0]-5*math.cos(angle)),round(b[1]-5*math.sin(angle)))
        wings=[(round(tip[0]-5*math.cos(angle+d)),round(tip[1]-5*math.sin(angle+d)))
               for d in (-.45,.45)]
        canvas.line([a,tip],LIGHT)
        canvas.poly([tip,*wings],LIGHT)
    for i,(x,y) in enumerate(nodes):
        canvas.bevel(x-4,y-4,9,9,GOLD if i==active else MOSS,2)


def series(canvas, points, *, x_range, y_range, source, box=(42,16,230,81)):
    """Plot supplied (x, y) points with explicit limits. Never interpolate missing data."""
    if not isinstance(source,Source):
        raise TypeError('A Source is required for a data series')
    xmin,xmax=x_range
    ymin,ymax=y_range
    x,y,w,h=box
    if not (xmin<xmax and ymin<ymax and w>0 and h>0):
        raise ValueError('Invalid chart bounds')
    canvas.line([(x,y),(x,y+h),(x+w,y+h)],LIGHT)
    for a,b in points:
        if not (xmin<=a<=xmax and ymin<=b<=ymax):
            raise ValueError('Point falls outside the declared axis ranges')
        px=x+round((a-xmin)/(xmax-xmin)*w)
        py=y+h-round((b-ymin)/(ymax-ymin)*h)
        canvas.bevel(px-2,py-2,5,5,GOLD,1)


def credit(caption, source, scale):
    caption_text(caption,9,111,source.citation,9,scale,outline=True)
