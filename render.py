import argparse
import math
from pathlib import Path
import subprocess

from PIL import Image
from art import Canvas, GOLD, LIGHT, INK
from character import ACTIONS, OUTFITS, Robot, sprite, sprite_layers
from expressions import EXPRESSIONS
from lab import SIZE, background, chair, desk

FPS=24
DURATION=10
ROOT=Path(__file__).resolve().parent

def smooth(x):
    return x*x*(3-2*x)

def question(c,x,y):
    points=[(x,y+3),(x+2,y),(x+7,y),(x+10,y+3),(x+10,y+6),
            (x+5,y+10),(x+5,y+12)]
    c.line(points,INK,5)
    c.line(points,GOLD,3)
    c.rect(x+3,y+15,5,5,INK)
    c.rect(x+4,y+16,3,3,GOLD)
    c.rect(x+3,y,4,1,LIGHT)

def frame(t,room):
    c=Canvas(SIZE)
    c.paste(room,0,0)
    chair(c)
    robot=Robot()
    turn=0
    if t<3.25:
        progress=t/3.25
        x=round(22+95*(0.8*progress+0.2*smooth(progress)))
        y=round(84-6*progress)
        action='walk'
        index=int(t*10)
        seated=False
    else:
        x=117
        y=78
        seated=t>=3.55
        if seated:
            y+=round(7*smooth(min(1,(t-3.55)/.4)))-4
        action='idle' if t<4.0 else 'read'
        index=int(t*8)
        if t>=4:
            robot.set_expression('focused')
        if 6.6<=t<7.45:
            robot.set_expression('confused')
        if t>=7.45:
            robot.set_expression('surprised')
            y-=round(2*math.sin(math.pi*min(1,(t-7.45)/.35)))
        for mark in (4.55,5.75):
            if mark<=t<mark+.48:
                turn=round(5*math.sin(math.pi*(t-mark)/.48))
    c.bevel(x+15,y+71,51,5,'#805b47',2)
    # The paper sits on the robot's lap. Both hands come from the character rig.
    c.paste(robot.render(action,index,seated=seated,page_turn=turn,
                         emotion_frame=int(t*12)),x,y)
    table=Canvas(SIZE)
    desk(table,papers=False)
    c.paste(table.image,22,8)
    if t>=7.65:
        pop=min(1,(t-7.65)/.28)
        question(c,177,66-round(9*smooth(pop))+round(math.sin((t-7.65)*4)))
    return c.image

def export_assets():
    assets=ROOT/'assets'
    for name in ('outfits','actions','scenes','expressions','layers'):
        (assets/name).mkdir(parents=True,exist_ok=True)
    poses={'scholar':'read','thinking':'think','outreach':'happy','crop':'happy'}
    for number,outfit in enumerate(OUTFITS,1):
        sprite(poses.get(outfit,'idle'),0,outfit).save(assets/'outfits'/f'{number:02d}-{outfit}.png')
    for action,(count,_) in ACTIONS.items():
        # Four columns, frame order left-to-right then top-to-bottom.
        sheet=Canvas((320,76*math.ceil(count/4)))
        for i in range(count):
            sheet.paste(sprite(action,i),80*(i%4),76*(i//4))
        sheet.image.save(assets/'actions'/f'{action}.png')
    preview=Canvas((320,320),'#c9a47c')
    for index,name in enumerate(EXPRESSIONS):
        image=sprite(expression=name)
        image.save(assets/'expressions'/f'{name}.png')
        preview.paste(image,80*(index%4),80*(index//4))
    preview.image.resize((960,960),Image.Resampling.NEAREST).save(assets/'expression-sheet.png')
    for name,image in sprite_layers().items():
        image.save(assets/'layers'/f'{name}.png')
    room=background()
    room.save(assets/'scenes'/'lab-background.png')
    furniture=Canvas(SIZE)
    chair(furniture)
    furniture.image.save(assets/'scenes'/'lab-chair.png')
    furniture=Canvas(SIZE)
    desk(furniture)
    furniture.image.save(assets/'scenes'/'lab-desk.png')

def export_video():
    output=ROOT/'output'
    output.mkdir(exist_ok=True)
    room=background()
    frame(8.4,room).resize((1280,720),Image.Resampling.NEAREST).save(output/'lab-still.png')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','rgb24','-video_size','320x180','-framerate',str(FPS),
         '-i','pipe:0','-vf','scale=1280:720:flags=neighbor','-an','-c:v','libx264',
         '-crf','14','-pix_fmt','yuv420p','-movflags','+faststart',str(output/'lab-test.mp4')]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as encoder:
        with encoder.stdin:
            for i in range(FPS*DURATION):
                encoder.stdin.write(frame(i/FPS,room).convert('RGB').tobytes())
        if encoder.wait():
            raise SystemExit('FFmpeg export failed')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--assets-only',action='store_true',help='Generate PNGs without FFmpeg')
    args=parser.parse_args()
    export_assets()
    if not args.assets_only:
        export_video()
