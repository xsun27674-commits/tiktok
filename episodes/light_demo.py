"""A short schematic about plants and light. All artwork is authored on the pixel grid."""
import math
from art import Canvas, GOLD, LIGHT, MOSS
from studio.graphics import Paper, label, text
from studio.timeline import Cue, Episode


def story_scene(local_beat, pulse):
    c=Canvas((320,180),'#243e3b')
    for y,color in ((22,'#2a4a45'),(46,'#32554b'),(76,'#3c6150'),(106,'#557455')):
        c.rect(0,y,320,180-y,color)
    for x,y in ((9,42),(41,61),(66,34),(105,60),(207,64),(247,29),(291,79),(304,47)):
        c.rect(x,y,1,1,'#88a475')
    c.poly([(0,116),(24,92),(54,99),(75,87),(105,107),(135,98),(169,106),
            (196,92),(221,113),(252,103),(281,90),(319,107),(319,179),(0,179)],'#415e48')
    c.rect(0,122,320,58,'#273d35')
    c.rect(0,122,320,2,'#78935b')
    if local_beat<10:
        label(c,13,10,'故事场景 · 光照')
        c.bevel(232,29,24,24,'#b99055',7)
        c.bevel(235,31,19,19,GOLD,6)
        c.bevel(239,34,10,10,LIGHT,3)
        for x,y,w,h in ((242,21,2,4),(242,56,2,4),(224,40,4,2),(260,40,4,2)):
            c.rect(x,y,w,h,GOLD)
        for i in range(3):
            step=(local_beat/4+i/3)%1
            x=round(226-step*86)
            y=round(50+step*31)
            c.line([(x,y),(x-7,y+4)],LIGHT if pulse>.65 else GOLD)
        c.line([(146,116),(146,85),(152,71)],'#283c33',4)
        c.line([(146,115),(146,86),(152,72)],'#91a964',2)
        c.poly([(150,83),(157,72),(170,66),(181,66),(177,76),(163,84)],'#263d32')
        c.poly([(152,82),(160,73),(169,69),(177,68),(173,75),(161,82)],'#a2ba60')
        c.line([(154,81),(171,72)],MOSS)
        c.poly([(146,94),(135,82),(121,78),(113,80),(118,90),(128,97),(144,98)],'#263d32')
        c.poly([(143,95),(135,85),(121,81),(116,82),(121,89),(130,94)],'#82a856')
        c.line([(122,85),(140,94)],MOSS)
        c.poly([(129,108),(163,108),(158,121),(135,121)],'#b77450')
        c.rect(128,106,36,4,'#d99c64')
        c.rect(138,112,3,7,'#e1a26c')
    else:
        label(c,13,10,'示意图 · 光合作用')
        c.poly([(54,81),(67,62),(91,47),(116,43),(157,42),(199,34),(241,36),
                (262,38),(249,58),(221,84),(195,96),(161,103),(114,107),(85,103),(65,94)],'#273f32')
        c.poly([(58,81),(71,64),(93,50),(117,46),(158,45),(201,37),(239,39),
                (256,40),(246,56),(220,81),(193,93),(160,100),(113,104),(86,100),(68,92)],'#7c9e54')
        c.line([(64,87),(111,82),(169,72),(242,48)],'#b6c978',2)
        for x,y in ((96,69),(130,58),(151,83),(180,57),(201,73),(227,48)):
            c.bevel(x,y,14,8,'#4a7444',3)
            c.line([(x+3,y+4),(x+10,y+3)],'#a0bb6a',2)
        for i in range(4):
            x=90+i*39
            y=round(56+10*math.sin(local_beat*1.2+i*2))
            c.bevel(x,y,4,4,GOLD if pulse>.5 else '#d1b363',1)
        text(c,116,108,'叶片把光能转为化学能',10,LIGHT)
    return c.image


EPISODE = Episode(
    title='叶子如何利用光？',
    intro=(Cue(0,'欢迎来到科研小屋！', 'happy','wave'),
           Cue(6,'阳光落在叶子上，\n它会变成什么？','confused','think')),
    story=(Cue(14,'叶绿素能吸收光。','focused'),
           Cue(19,'先看阳光照到叶片。','inspired','wave'),
           Cue(24,'叶片里的变化',visible=False),
           Cue(28,'光能支持植物\n把水和二氧化碳转化为糖。','excited')),
    summary=(Cue(36,'叶片把光能转成化学能，\n把能量储存在糖里。','focused'),
             Cue(44,'下次见！','happy','wave')),
    story_start=14, summary_start=36, end=52, story_scene=story_scene,
)

# Standalone card layout example, separate from the non-paper demo episode.
PAPER_EXAMPLE = Paper(
    'A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species',
    'G. D. Farquhar, S. von Caemmerer, J. A. Berry',
    'Planta', 1980, '10.1007/BF00386231',
)
