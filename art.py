from PIL import Image, ImageDraw

INK='#352821'; CREAM='#ffe9b6'; LIGHT='#fff7db'; SHADE='#d8ae7f'
SCREEN='#38272a'; GOLD='#ffcf71'; BLUSH='#e88a65'
GREEN='#688844'; MOSS='#405638'; LIME='#a9c65a'

class Canvas:
    def __init__(self, size, color=None):
        self.image=Image.new('RGBA',size,color or (0,0,0,0))
        self.d=ImageDraw.Draw(self.image)

    def rect(self,x,y,w,h,c):
        self.d.rectangle((x,y,x+w-1,y+h-1),fill=c)

    def poly(self,points,c):
        self.d.polygon(points,fill=c)

    def line(self,points,c,width=1):
        self.d.line(points,fill=c,width=width)

    def bevel(self,x,y,w,h,c,k=3):
        self.poly([(x+k,y),(x+w-k-1,y),(x+w-1,y+k),(x+w-1,y+h-k-1),
                   (x+w-k-1,y+h-1),(x+k,y+h-1),(x,y+h-k-1),(x,y+k)],c)

    def paste(self,image,x,y):
        self.image.alpha_composite(image,(x,y))
