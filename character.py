import math
from art import Canvas, INK, CREAM, LIGHT, SHADE, SCREEN, GOLD, BLUSH, GREEN, MOSS, LIME

OUTFITS=('base','scholar','experiment','ai','field','micro','crop','thinking','outreach','daily')
ACTIONS={'idle':(12,3), 'blink':(6,12), 'walk':(8,10), 'wave':(12,10),
         'read':(12,8), 'think':(12,5), 'surprise':(8,10), 'happy':(12,8),
         'microscope':(12,6), 'sprout':(12,6)}

def paper(c,x,y,turn=0):
    c.poly([(x,y+1),(x+11,y),(x+22,y+2),(x+22,y+9),(x+11,y+8),(x,y+9)],INK)
    c.poly([(x+1,y+1),(x+10,y),(x+11,y+2),(x+12,y),(x+21,y+2),(x+21,y+7),
            (x+12,y+6),(x+11,y+7),(x+1,y+8)],LIGHT)
    for offset in (3,5):
        c.line([(x+3,y+offset),(x+8,y+offset-1)],'#aa976d')
        c.line([(x+14,y+offset-1),(x+19,y+offset)],'#aa976d')
    if turn:
        c.poly([(x+11,y+1),(x+12+turn,y-2-turn),(x+20,y-1-turn),(x+16,y+4),(x+11,y+6)],CREAM)
        c.line([(x+11,y+1),(x+12+turn,y-2-turn),(x+20,y-1-turn)],SHADE)

def microscope(c,x,y):
    c.bevel(x,y+17,19,4,INK,1)
    c.rect(x+2,y+17,15,2,'#798679')
    c.line([(x+13,y+5),(x+16,y+8),(x+16,y+13),(x+12,y+17)],INK,4)
    c.line([(x+13,y+5),(x+15,y+8),(x+15,y+13),(x+12,y+16)],'#879b8a',2)
    c.poly([(x+6,y),(x+12,y+2),(x+9,y+9),(x+4,y+7)],INK)
    c.line([(x+9,y+2),(x+7,y+6)],'#c9d7bd',3)
    c.rect(x+6,y+9,3,3,'#9f9c84')
    c.rect(x+3,y+13,11,2,INK)
    c.rect(x+5,y+12,6,1,'#99ccaa')

def sprite(action='idle',frame=0,outfit='base',seated=False,facing=1,prop=True):
    count,_=ACTIONS[action]
    phase=frame%count
    sway=round(math.sin(phase*math.tau/count))
    bob=int(phase in (1,2,5,6)) if action=='walk' else int(action in ('idle','happy') and 3<=phase<=7)
    if action in ('microscope','think'):
        bob=int(phase in (3,4,5,6,7,8))
    elif action=='surprise':
        bob=-(1 if phase==1 else 0)
    c=Canvas((80,76))
    y=bob+(4 if seated else 0)
    swing=(-4,-3,0,3,4,3,0,-3)[phase] if action=='walk' else 0
    fy=69 if seated else 66
    for x,step in ((24,swing),(43,-swing)):
        lift=1 if action=='walk' and step<0 else 0
        c.bevel(x+step,fy-lift,13,6,INK,2)
        c.rect(x+2+step,fy+1-lift,9,3,MOSS)
        c.rect(x+3+step,fy+1-lift,5,1,'#98a565')
    # Canvas backpack and coat share the same body rig across costumes.
    c.bevel(16,48+y,16,20,INK,3)
    c.bevel(17,49+y,13,17,'#777746',2)
    c.rect(19,53+y,3,9,'#9c975a')
    c.bevel(23,46+y,34,23,INK,4)
    c.bevel(25,47+y,30,20,CREAM,3)
    c.rect(27,64+y,26,3,SHADE)
    c.poly([(30,47+y),(39,48+y),(47,47+y),(40,58+y)],MOSS)
    c.line([(30,47+y),(33,54+y),(40,58+y),(47,51+y)],INK,2)
    c.line([(40,57+y),(40,66+y)],INK)
    c.rect(46,59+y,6,4,SHADE)
    c.rect(47,59+y,4,3,LIGHT)
    c.line([(49,60+y),(49,55+y)],MOSS)
    c.rect(47,55+y,2,2,GREEN)
    c.rect(50,54+y,2,2,LIME)
    c.line([(24,60+y),(29,53+y),(29,49+y)],'#856043',2)

    arms=[(23+swing//2,56+y),(54-swing//2,56+y)]
    if action=='wave':
        arms[1]=(59+(phase%4-2),43+abs(5-phase)//2+y)
    if action=='think':
        arms[1]=(51,47+y)
    if action in ('read','microscope'):
        arms=[(28,59+y),(52,58+y)]
    if action=='happy':
        arms=[(20,52+y),(57,52+y)]
    for x,ay in arms:
        c.bevel(x-4,ay,9,11,INK,2)
        c.bevel(x-3,ay+1,7,9,CREAM,2)
        c.rect(x-1,ay+2,3,2,LIGHT)
        c.rect(x-2,ay+8,5,1,SHADE)

    h=19+y
    lean=sway if action in ('sprout','walk','idle') else 0
    c.line([(40,h+3),(40,h-5),(38+lean,h-11)],MOSS,3)
    c.line([(41,h+1),(41,h-5),(47+lean,h-11)],GREEN,2)
    c.poly([(40,h-7),(34+lean,h-6),(28+lean,h-8),(24+lean,h-12),(24+lean,h-16),
            (28+lean,h-17),(34+lean,h-16),(39+lean,h-12)],MOSS)
    c.poly([(39,h-8),(32+lean,h-8),(27+lean,h-11),(25+lean,h-15),(30+lean,h-16),
            (35+lean,h-14)],LIME)
    c.line([(28+lean,h-13),(35+lean,h-11),(39,h-8)],GREEN)
    c.poly([(41,h-8),(44+lean,h-14),(49+lean,h-18),(55+lean,h-18),(57+lean,h-16),
            (55+lean,h-11),(50+lean,h-8)],MOSS)
    c.poly([(43,h-9),(46+lean,h-14),(50+lean,h-17),(55+lean,h-17),(55+lean,h-14),
            (51+lean,h-10)],'#b8c16b')
    c.line([(43,h-9),(51+lean,h-14)],GREEN)
    # Stepped shell, inset glass and recessed ear housings.
    c.bevel(13,h,53,33,INK,8)
    c.bevel(14,h+1,51,31,SHADE,7)
    c.bevel(15,h+1,50,28,CREAM,7)
    c.line([(24,h+2),(50,h+2),(53,h+3)],LIGHT,2)
    c.line([(20,h+8),(22,h+5),(25,h+4)],LIGHT)
    c.bevel(28,h+7,34,22,'#997454',5)
    c.bevel(29,h+8,33,20,SCREEN,4)
    c.line([(31,h+13),(32,h+10),(36,h+9)],'#765457')
    c.rect(56,h+11,3,1,'#594045')
    for x,w in ((11,11),(64,5)):
        c.bevel(x,h+11,w,16,INK,3)
        c.bevel(x+1,h+12,w-2,14,MOSS,2)
        c.rect(x+2,h+14,2,8,GREEN)
        if w>5:
            c.rect(x+5,h+15,2,5,'#abb66a')
    for x in (33,55):
        c.bevel(x,h+22,5,2,BLUSH,1)
    for x in (38,52):
        if action=='blink' and phase in (2,3):
            c.rect(x-1,h+17,4,1,GOLD)
        elif action=='happy':
            c.line([(x-2,h+18),(x,h+15),(x+2,h+18)],GOLD)
        elif action=='think':
            direction=1 if x==38 else -1
            c.line([(x-direction*2,h+14),(x+direction*2,h+16),(x-direction*2,h+18)],GOLD)
        elif action=='surprise':
            c.bevel(x-1,h+12,5,8,GOLD,1)
            c.rect(x,h+13,1,3,LIGHT)
        else:
            ey=h+16 if action in ('read','microscope') else h+13
            c.bevel(x,ey,3,7,GOLD,1)
            c.rect(x+1,ey+1,1,2,LIGHT)
    if action=='surprise':
        c.bevel(44,h+20,4,5,BLUSH,1)
        c.rect(45,h+21,2,3,INK)

    accessories(c,outfit,h)
    if prop and (action=='read' or outfit=='scholar'):
        paper(c,29,60+y,(0,1,3,4,3,1)[phase-4] if action=='read' and 4<=phase<=9 else 0)
    if prop and action=='microscope':
        microscope(c,53,49)
    if facing==-1:
        from PIL import Image
        return c.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return c.image

def accessories(c,outfit,h):
    if outfit in ('scholar','experiment'):
        top=h+9 if outfit=='scholar' else h-4
        for x in (31,47):
            c.bevel(x,top,15,13,INK,4)
            c.bevel(x+1,top+1,13,11,'#e6ded0',4)
            c.bevel(x+3,top+3,9,7,SCREEN if outfit=='scholar' else '#6f8790',2)
            if outfit=='scholar':
                c.rect(x+7,top+4,2,5,GOLD)
            else:
                c.line([(x+4,top+7),(x+7,top+4)],LIGHT)
        if outfit=='experiment':
            c.poly([(65,57),(69,57),(69,61),(74,69),(72,72),(62,72),(60,69),(65,61)],LIGHT)
            c.poly([(64,65),(70,65),(72,69),(70,71),(63,71),(62,69)],LIME)
    if outfit in ('ai','daily'):
        c.line([(15,h+13),(15,h+5),(23,h-1),(49,h-2),(61,h+2),(66,h+12)],INK,3)
        c.line([(15,h+9),(19,h+2),(26,h-2),(49,h-3),(60,h+1)],SHADE,2)
        for x in (10,63):
            c.bevel(x,h+13,8,12,GOLD,2)
            c.rect(x+2,h+16,4,6,GREEN)
    if outfit=='ai':
        c.poly([(31,56),(56,56),(61,69),(34,69)],INK)
        c.poly([(33,57),(55,57),(59,67),(35,67)],'#888b84')
        c.line([(45,64),(45,60),(49,59)],LIME)
    if outfit in ('field','crop'):
        c.poly([(11,h+5),(20,h-1),(26,h-7),(35,h-9),(50,h-8),(57,h-4),(65,h+1),
                (71,h+4),(68,h+8),(54,h+5),(24,h+5),(14,h+9)],INK)
        c.poly([(13,h+5),(22,h-1),(28,h-6),(36,h-8),(49,h-7),(56,h-3),(68,h+4),
                (63,h+5),(51,h+2),(24,h+3),(15,h+7)],'#dfa764')
        c.line([(22,h+1),(35,h-3),(51,h-3),(61,h+1)],SHADE,2)
        if outfit=='field':
            c.bevel(28,56,15,12,INK,2)
            c.bevel(30,57,11,10,'#8b624e',2)
            c.bevel(32,58,8,8,INK,2)
            c.rect(34,60,3,3,'#8b9b91')
        else:
            for x in (13,17,20):
                c.line([(21,70),(x,48)],SHADE)
                for yy in (49,53,57):
                    c.poly([(x,yy+2),(x-3,yy),(x-3,yy-2),(x,yy-1),(x+2,yy-3),(x+3,yy-1)],GOLD)
    if outfit=='micro':
        c.line([(13,h+28),(7,h+21),(7,h+5),(12,h-6),(22,h-13),(34,h-16),
                (49,h-16),(61,h-11),(70,h-1),(74,h+11),(73,h+23),(65,h+31)],
               '#969aad',3)
        c.line([(10,h+6),(15,h-5),(23,h-10),(30,h-12)],'#e3e4ef',2)
        c.bevel(43,55,10,9,'#747b8a',2)
        c.rect(46,57,4,4,'#94c2bc')
    if outfit=='thinking':
        c.poly([(55,52),(69,54),(65,70),(51,67)],LIGHT)
        c.line([(56,63),(62,61),(58,56),(65,56)],GREEN)
    if outfit=='outreach':
        c.line([(54,65),(72,43)],INK,3)
        c.line([(54,64),(71,44)],GOLD)
    if outfit=='daily':
        c.bevel(22,h+29,38,8,'#a56e38',2)
        c.rect(24,h+30,34,3,'#e4a74f')
        for x in (26,34,42,50):
            c.rect(x,h+30,2,5,'#ba813d')
        c.bevel(59,54,14,13,INK,2)
        c.bevel(60,55,11,11,CREAM,2)
        c.line([(65,62),(65,58),(68,57)],GREEN)
