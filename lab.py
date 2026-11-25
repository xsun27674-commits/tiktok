from art import Canvas, INK, CREAM, LIGHT, GOLD, GREEN, MOSS, LIME
from character import microscope, paper

SIZE=(320,180)
WOOD='#895639'; EDGE='#52382e'; TOP='#c78b54'; WALL='#dcb789'
TEAL='#50726a'; DARK_TEAL='#304d4c'

def plant(c,x,y,scale=1):
    for dx,dy in ((-5,-13),(3,-16),(9,-9),(-9,-7),(1,-21)):
        c.line([(x,y),(x+dx*scale,y+dy*scale)],MOSS,scale)
        xx=x+dx*scale
        yy=y+dy*scale
        c.poly([(xx-4*scale,yy-2*scale),(xx,yy-2*scale),(xx+4*scale,yy+scale),
                (xx+3*scale,yy+3*scale),(xx-scale,yy+3*scale)],GREEN)
        c.line([(xx-2*scale,yy-scale),(xx+scale,yy)],LIME,scale)
    c.poly([(x-8*scale,y),(x+8*scale,y),(x+6*scale,y+9*scale),(x-6*scale,y+9*scale)],EDGE)
    c.poly([(x-7*scale,y+scale),(x+7*scale,y+scale),(x+5*scale,y+8*scale),(x-5*scale,y+8*scale)],'#bd7350')
    c.rect(x-8*scale,y,16*scale,2*scale,'#e09767')
    c.rect(x-5*scale,y+3*scale,2*scale,4*scale,'#db9261')

def bookshelf(c):
    c.rect(20,26,76,73,'#bc916b')
    c.bevel(17,22,76,75,EDGE,2)
    c.rect(20,25,70,69,WOOD)
    for bottom in (47,69,91):
        c.rect(22,bottom-18,66,18,'#664732')
        c.rect(22,bottom-17,66,2,'#573d2d')
        x=25
        for index,(height,width,color) in enumerate([
            (13,5,TEAL),(15,6,'#a4654e'),(11,4,'#b99a58'),(14,6,'#7f9258'),
            (10,5,'#ca9064'),(13,5,'#768982')]):
            height-=((bottom+index)%3)
            c.rect(x,bottom-height,width,height,color)
            c.rect(x+1,bottom-height+2,width-2,1,'#d6bc82')
            c.rect(x+1,bottom-3,width-2,1,EDGE)
            x+=width+1
        if bottom==47:
            plant(c,76,40)
        elif bottom==69:
            for i in range(3):
                c.rect(70+i*5,bottom-11+i,3,11-i,'#b8ccc0')
                c.rect(70+i*5,bottom-4,3,3,TEAL)
        else:
            c.rect(69,84,15,6,'#c48750')
            c.rect(71,85,11,2,'#e4bb7d')
        c.rect(19,bottom,72,3,TOP)
        c.rect(19,bottom+2,72,1,EDGE)
    c.rect(19,23,71,2,TOP)

def window(c):
    c.bevel(115,15,89,66,'#bb956e',3)
    c.bevel(111,11,89,66,EDGE,3)
    c.rect(114,14,83,60,TOP)
    c.rect(117,17,77,54,'#779c99')
    c.rect(117,39,77,32,'#94b4a3')
    c.rect(117,52,77,19,'#bfd0aa')
    c.bevel(171,20,15,15,'#ffe0a1',5)
    for x,y in ((124,29),(154,42),(178,38)):
        c.rect(x,y,14,2,'#c8d7ba')
        c.rect(x+3,y-2,7,2,'#c8d7ba')
    c.poly([(117,64),(129,52),(141,56),(149,62),(161,53),(171,53),(193,66),(193,71),(117,71)],'#719284')
    c.poly([(117,67),(125,64),(136,66),(149,61),(167,67),(182,59),(193,64),(193,71),(117,71)],'#597c70')
    for x,y in ((122,62),(139,66),(180,64),(188,61)):
        c.line([(x-3,y),(x,y-7),(x+3,y)],'#4b6b60',2)
    c.rect(154,15,3,59,EDGE)
    c.rect(154,15,1,59,TOP)
    c.rect(115,46,81,3,EDGE)
    c.rect(115,46,81,1,TOP)
    c.rect(109,73,94,5,EDGE)
    c.rect(110,73,92,2,'#e0aa6a')

def monitor(c,x,y):
    c.bevel(x,y,32,24,INK,3)
    c.bevel(x+1,y+1,30,21,TEAL,2)
    c.rect(x+4,y+4,24,15,DARK_TEAL)
    for row in range(3):
        c.rect(x+6,y+7+row*3,6+row,1,'#92ac87')
    c.line([(x+17,y+15),(x+20,y+11),(x+23,y+13),(x+26,y+7)],'#c4c775')
    c.rect(x+26,y+20,2,1,GOLD)
    c.rect(x+14,y+24,5,6,EDGE)
    c.bevel(x+9,y+29,15,3,TEAL,1)

def background():
    c=Canvas(SIZE,WALL)
    for y,color in ((0,'#c89c75'),(7,'#e7c69a'),(77,'#e7c195'),(95,'#c89b72'),(98,'#e7bd8d')):
        c.rect(0,y,320,2,color)
    for x in range(8,320,19):
        c.rect(x,10,1,85,'#d4ac80')
    c.rect(0,99,320,4,EDGE)
    for x in range(0,320,14):
        c.rect(x,104,13,25,'#a17756' if x%28 else '#a77c59')
        c.rect(x,105,1,21,'#bc8f64')
    c.rect(0,126,320,4,'#654539')
    c.rect(0,130,320,50,'#a67957')
    for row,y in enumerate((133,141,151,163,177)):
        c.rect(0,y,320,1,'#835c4a')
        c.rect(0,y+1,320,1,'#bd8e62')
        for x in range((row*31)%57,320,57):
            c.line([(x,y+2),(x-3,min(179,y+9))],'#885f49')
            if x+20<320:
                c.rect(x+11,y+4,10,1,'#b2845c')
    c.poly([(116,131),(194,131),(227,179),(82,179)],'#bb9062')
    c.poly([(128,135),(186,135),(209,176),(107,176)],'#c69b69')
    bookshelf(c)
    window(c)
    # Framed botanical specimen.
    c.bevel(226,16,42,46,EDGE,2)
    c.rect(228,18,38,42,TOP)
    c.rect(231,21,32,36,'#e7c490')
    c.rect(234,24,26,30,'#f5d9a6')
    c.line([(244,50),(248,42),(247,31)],MOSS)
    for x,y in ((241,41),(253,36),(244,33),(253,43)):
        c.poly([(247,y+4),(x-3,y),(x-2,y-3),(x+2,y-3),(x+3,y)],GREEN)
    c.rect(238,52,7,1,TOP)
    c.rect(249,52,6,1,TOP)
    # Rear lab station.
    c.bevel(213,96,101,36,EDGE,3)
    c.rect(216,101,95,27,TEAL)
    for x in (218,250,282):
        c.rect(x,103,29,23,DARK_TEAL)
        c.rect(x+1,104,27,21,TEAL)
        c.rect(x+10,108,9,2,'#beab7d')
    c.rect(210,94,106,5,TOP)
    c.rect(210,98,106,2,EDGE)
    monitor(c,270,62)
    microscope(c,225,73)
    for x,color in ((250,'#6e9a79'),(261,'#d99b60')):
        c.poly([(x+3,76),(x+6,76),(x+6,81),(x+10,90),(x+9,93),(x,93),(x-1,90),(x+3,81)],'#c5d2b4')
        c.poly([(x+2,87),(x+7,86),(x+9,91),(x,91)],color)
        c.rect(x+2,75,6,2,LIGHT)
    plant(c,19,123,2)
    plant(c,307,85)
    return c.image

def chair(c):
    c.bevel(125,114,33,35,EDGE,3)
    c.bevel(127,116,29,29,'#7c8868',2)
    c.rect(129,118,1,25,'#a2a07a')
    c.rect(135,146,3,14,EDGE)
    c.rect(165,146,3,14,EDGE)
    c.bevel(132,142,38,7,EDGE,2)
    c.rect(134,142,32,3,'#a1946c')

def desk(c,turn=0,focus=False,*,papers=True):
    for x in (182,268):
        c.rect(x,130,6,33,EDGE)
        c.rect(x+1,132,2,29,WOOD)
    c.rect(180,129,96,9,EDGE)
    c.rect(182,130,92,5,WOOD)
    c.poly([(173,129),(185,116),(277,116),(280,129)],EDGE)
    c.poly([(175,128),(186,117),(275,117),(278,127)],TOP)
    c.line([(176,128),(277,128)],'#e9ab69')
    c.line([(210,126),(250,126)],'#b6794a')
    # Lamp shade and pool of light use hard-edged shapes.
    c.bevel(255,121,15,4,EDGE,2)
    c.line([(262,121),(264,101),(251,89),(241,94)],EDGE,3)
    c.line([(263,117),(265,101),(252,89),(243,93)],'#a28b58')
    c.poly([(232,96),(235,89),(240,86),(245,89),(248,96)],DARK_TEAL)
    c.rect(232,96,17,2,EDGE)
    c.rect(235,96,11,1,LIGHT)
    c.poly([(236,117),(246,117),(257,126),(222,126)],'#df9f5d')
    if papers:
        paper(c,186,118,turn)
    c.bevel(220,119,13,5,EDGE,1)
    c.rect(221,119,11,2,'#879568')
    c.rect(222,122,10,1,CREAM)
    if focus and papers:
        c.rect(197,123,3,1,GOLD)
