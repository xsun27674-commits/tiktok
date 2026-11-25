"""Original, softly enveloped game-audio cues. Frequencies are MIDI notes."""
from array import array
import math
import random
import sys
import wave

RATE=24000
MOTIF=(72,76,79)
CUES={
    'opening': ((0,MOTIF[0],.29),(.16,MOTIF[1],.32),(.33,MOTIF[2],.46)),
    'paper': ((0,81,.18),(.08,88,.28)),
    'sprout': ((0,67,.28),(.10,71,.32),(.21,74,.38),(.33,79,.56)),
    'discovery': ((0,76,.48),(.075,83,.34),(.16,88,.42)),
    'stamp': ((0,43,.22),),
    'ending': ((0,MOTIF[0]-12,.42),(.27,MOTIF[1]-12,.47),(.56,MOTIF[2]-12,.65)),
}


def write(path,duration,events):
    mix=[0.]*round(duration*RATE)
    for onset,cue in events:
        for offset,note,length in CUES[cue]:
            start=round((onset+offset)*RATE)
            freq=440*2**((note-69)/12)
            rng=random.Random(note)
            noise=0.
            for i in range(round(length*RATE)):
                if start+i>=len(mix):
                    break
                t=i/RATE
                envelope=min(1,t/.015)*math.exp(-4*t/length)*min(1,(length-t)/.04)
                phase=math.tau*freq*t
                tone=.77*math.sin(phase)+.17*math.sin(phase*2)+.06*math.sin(phase*3)
                if cue=='stamp':
                    noise=.92*noise+.08*rng.uniform(-1,1)
                    tone=.46*math.sin(phase)+2.8*noise
                mix[start+i]+=tone*envelope*(.11 if cue=='ending' else .18)
    pcm=array('h',(round(32767*max(-1,min(1,value))) for value in mix))
    if sys.byteorder!='little':
        pcm.byteswap()
    with wave.open(str(path),'wb') as out:
        out.setparams((1,2,RATE,0,'NONE','not compressed'))
        out.writeframes(pcm.tobytes())
