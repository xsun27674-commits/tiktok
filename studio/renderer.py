"""Render fixed brand shots around a swappable, beat-indexed story scene."""
from bisect import bisect_right
from pathlib import Path
from subprocess import Popen, run
from tempfile import TemporaryDirectory
import math
import wave
from array import array

from PIL import Image
from art import Canvas
from character import ACTIONS, Robot
from lab import background, desk
from studio.graphics import WIDTH, HEIGHT, curtain, dialogue, subtitle, paper_card
from studio.timeline import BeatClock

FPS=24
STORY_HOST_AREA=(0,124,320,180)
TRANSITION_BEATS=2
SIZE=(WIDTH,HEIGHT)


def at_beat(cues,beat):
    return cues[bisect_right([cue.beat for cue in cues],beat)-1]


def brand_room():
    c=Canvas(SIZE)
    c.paste(background(),0,0)
    desk(c,papers=False)
    return c.image


class Program:
    def __init__(self, episode):
        self.episode=episode
        self.clock=BeatClock(episode.bpm)
        self.room=brand_room()
        self.robot=Robot()
        self.total_frames=round(self.clock.seconds(episode.end)*FPS)
        boundaries=(0,episode.story_start,episode.summary_start,episode.end)
        for cues,start,end in zip((episode.intro,episode.story,episode.summary),
                                  boundaries,boundaries[1:]):
            beats=[cue.beat for cue in cues]
            if not beats or beats[0]!=start or beats!=sorted(set(beats)) or beats[-1]>=end:
                raise ValueError('Cue beats must start at the section boundary and increase within it')
        if episode.paper:
            if (episode.paper_start is None or episode.farewell_start is None
                    or not episode.summary_start<episode.paper_start<episode.farewell_start<episode.end):
                raise ValueError('A paper card needs a display window before the farewell')
            if at_beat(episode.summary,episode.farewell_start).action!='wave':
                raise ValueError('The first shot after the paper card must use the wave action')
        self.card=paper_card(episode.paper) if episode.paper else None

    def character(self,c,cue,beat,x,y,small=False):
        elapsed=float(self.clock.seconds(beat-cue.beat))
        self.robot.set_expression(cue.expression)
        pose=self.robot.render(cue.action,int(elapsed*ACTIONS[cue.action][1]),
                               emotion_frame=int(elapsed*12))
        if small:
            pose=pose.resize((40,38),Image.Resampling.NEAREST)
        c.paste(pose,x,y)

    def frame(self,seconds):
        e=self.episode
        beat=self.clock.beat(seconds)
        pulse=self.clock.pulse(seconds)
        story=e.story_start<=beat<e.summary_start
        c=Canvas(SIZE)
        if story:
            c.paste(e.story_scene(beat-e.story_start,pulse),0,0)
            cue=at_beat(e.story,beat)
            if cue.visible:
                self.character(c,cue,beat,11,133,small=True)
                if cue.dialogue:
                    dialogue(c,cue.dialogue,x=55,y=142,w=207,tail=49,highlight=pulse>.55)
        elif self.card and e.paper_start<=beat<e.farewell_start:
            c.paste(self.card,0,0)
        else:
            intro=beat<e.story_start
            c.paste(self.room,0,0)
            cue=at_beat(e.intro if intro else e.summary,beat)
            if cue.visible:
                self.character(c,cue,beat,75,79)
                if cue.dialogue:
                    subtitle(c,cue.dialogue)
        for cut in (e.story_start,e.summary_start):
            delta=beat-cut
            if abs(delta)<TRANSITION_BEATS/2:
                curtain(c,.5+delta/TRANSITION_BEATS)
        return c.image


def write_music(path,program):
    """Generate an original, instrumental arpeggio on the show's beat grid."""
    rate=22050
    clock=program.clock
    span=program.total_frames/FPS
    tune=(60,64,67,72,67,64,62,65,69,74,69,65,59,62,67,71)
    samples=array('h')
    for i in range(round(rate*span)):
        t=i/rate
        beat=clock.beat(t)
        n=int(beat*2)
        age=(beat-n/2)*60/clock.bpm
        pitch=440*2**((tune[n%len(tune)]-69)/12)
        envelope=min(1,age/.018)*math.exp(-13*age)
        fade=min(1,t/.1,max(0,(span-t)/.6))
        tone=math.sin(math.tau*pitch*age)+.19*math.sin(math.tau*pitch*2*age)
        samples.append(round(3100*tone*envelope*fade))
    import sys
    if sys.byteorder!='little':
        samples.byteswap()
    with wave.open(str(path),'wb') as audio:
        audio.setparams((1,2,rate,0,'NONE','not compressed'))
        audio.writeframes(samples.tobytes())


def encode(program,output,music=None,generate_music=False):
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory() as tmp:
        if generate_music:
            music=Path(tmp)/'beat.wav'
            write_music(music,program)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
             '-pixel_format','rgb24','-video_size',f'{WIDTH}x{HEIGHT}',
             '-framerate',str(FPS),'-i','pipe:0']
        if music:
            cmd+=['-i',str(music),'-map','0:v:0','-map','1:a:0','-af','apad',
                  '-c:a','aac','-b:a','128k','-shortest']
        else:
            cmd+=['-an']
        cmd+=['-vf','scale=1280:720:flags=neighbor','-c:v','libx264','-crf','14',
              '-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
        with Popen(cmd,stdin=-1) as proc:
            with proc.stdin:
                for i in range(program.total_frames):
                    proc.stdin.write(program.frame(i/FPS).convert('RGB').tobytes())
            if proc.wait():
                raise RuntimeError('FFmpeg program export failed')
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
