"""Original cue arrangements for the brand music audition."""
from dataclasses import dataclass

# General MIDI presets: acoustic piano, music box, marimba, xylophone,
# nylon guitar, acoustic bass, warm pad, and sine-like lead.
PATCHES = (0, 10, 12, 13, 24, 32, 89, 80, 12, 0)
PAN = (63, 83, 41, 74, 47, 63, 66, 90, 57, 70)
LEVELS = (104, 73, 84, 66, 75, 92, 55, 39, 84, 95)
MOTIF = ((0,72,.78),(1,76,.60),(1.75,79,.66),(2.5,81,1.08),
         (4,79,.83),(5,76,.76),(5.9,74,.64),(6.7,72,1.2))

# Root notes with open voicings written for each cue.
HOME = ((48,(55,59,64,67)),(45,(55,59,60,64)),(41,(53,57,60,64)),
        (43,(55,57,62,65)),(48,(55,59,64,67)),(52,(55,59,62,67)),
        (41,(53,57,60,67)),(43,(55,60,62,65)),
        (45,(55,57,60,64)),(40,(52,55,59,62)),(41,(53,57,60,64)),
        (43,(55,57,60,62)),(48,(55,59,64,67)),(41,(53,57,60,64)),
        (43,(55,60,62,65)),(48,(52,55,60,62)))
EXPLORE = ((50,(57,60,64,65)),(46,(53,57,60,62)),(48,(55,60,62,64)),
           (45,(52,55,60,64)),(50,(53,57,60,64)),(43,(53,57,58,62)),
           (46,(53,57,60,65)),(45,(52,55,61,64)))*2
MICRO = ((45,(52,55,59,64)),(41,(52,55,57,60)),(48,(55,59,62,64)),
         (43,(54,57,62,64)),(45,(52,57,59,64)),(42,(52,57,59,64)),
         (41,(53,57,60,67)),(45,(52,55,59,64)))*2


@dataclass
class Cue:
    name: str
    bpm: int
    events: list

    def note(self,ch,beat,pitch,length,velocity):
        self.events.extend(((beat,ch,pitch,velocity),(beat+length,ch,pitch,0)))


def compose(style):
    bpm = (104,112,82,76)[style]
    cue=Cue(('01-research-cabin','02-science-adventure','03-microworld',
             '04-todays-discovery')[style],bpm,[])
    harmony=(HOME,EXPLORE,MICRO,HOME)[style]
    for bar,(root,chord) in enumerate(harmony):
        at=bar*4
        final=bar==15
        if style==0:
            cue.note(5,at,root,1.5,56 if bar%2 else 63)
            if not final:
                cue.note(5,at+2.5,root+12,.67,49)
            for j,index in enumerate((0,1,2,1,3,2) if not final else (0,1,2,3)):
                offset=(.08,.59,1.36,2.09,2.63,3.36)[j]
                cue.note(0,at+offset,chord[index],.58+(j%2)*.19,52-j*2+(bar%3)*2)
            if bar%2 and not final:
                cue.note(2,at+3.04,chord[1]+12,.38,44)
                cue.note(2,at+3.52,chord[2]+12,.39,37)
        elif style==1:
            for j,offset in enumerate((0,1.48,2.49)):
                cue.note(5,at+offset,root+(0,12,7)[j],.71,60-j*5)
            for j,index in enumerate((0,2,1,3,2,1)):
                offset=(.24,.75,1.25,1.98,2.74,3.49)[j]
                cue.note(2,at+offset,chord[index]+12,.33+(j%3)*.12,55+(2-j%4)*4)
            for offset in (1.75,3.25):
                for pitch in chord[1:3]:
                    cue.note(4,at+offset,pitch,.48,40)
        elif style==2:
            cue.note(5,at+.07,root,3.55,49)
            for j,pitch in enumerate(chord):
                cue.note(6,at+.15+j*.18,pitch,3.29-j*.21,45-j*2)
                cue.note(0,at+.31+j*.69,pitch+12,1.05,49-j*4)
            if not final:
                cue.note(7,at+2.71,chord[2]+24,.46,34)
                cue.note(1,at+3.31,chord[1]+24,.51,41)
        else:
            cue.note(0,at,root,2.96,48)
            for j,pitch in enumerate(chord):
                cue.note(0,at+.20+j*.55,pitch,1.8-(j*.24),51-j*3)
                if j>0:
                    cue.note(6,at+.39+j*.06,pitch,3.28,37-j)
            if bar%2==1 and not final:
                cue.note(1,at+2.9,chord[2]+12,.7,41)
                cue.note(1,at+3.44,chord[3]+12,.46,35)

    if style in (0,3):
        for section in (0,16,48):
            for i,(beat,pitch,length) in enumerate(MOTIF):
                if style==0:
                    cue.note(8,section+beat,pitch,length-(.11 if i%2 else 0),71-i%4*3)
                    if section:
                        cue.note(1,section+beat+.035,pitch+12,length*.75,42-i%3*3)
                else:
                    cue.note(0,section+beat+.035,pitch,length+.26,64-i%4*3)
                    if (i+section)%3==2:
                        cue.note(1,section+beat+.12,pitch+12,length*.75,40)
        bridge=(69,72,76,74,72,71,67,69)
        for i,pitch in enumerate(bridge):
            cue.note(4 if style==0 else 0,32+i*1.45,pitch,.91,56-i%4*3)
        cue.note(0,62,72,1.78,57)
    elif style==1:
        phrase=((0,69),(1,72),(1.74,74),(2.55,77),(4.55,76),(5.4,72),(6.24,69),
                (8,67),(8.75,72),(9.5,74),(10.45,76),(12,73),(13.15,72),(14.1,69))
        for section in (0,16,32,48):
            for i,(beat,pitch) in enumerate(phrase):
                cue.note(3,section+beat,pitch+(12 if section==32 and i<4 else 0),
                         .42 if i%3 else .78,65+(i%4)*3)
                if i%4==2:
                    cue.note(1,section+beat+.08,pitch+12,.54,43)
        cue.note(2,63,69,.86,49)
    else:
        phrase=((0,76),(1.55,79),(3.0,83),(5.0,81),(7.55,76),(9,74),(10.47,76),
                (12.7,79),(14.4,71))
        for section in (0,16,32,48):
            for i,(beat,pitch) in enumerate(phrase):
                cue.note(1,section+beat,pitch+12*(section==32 and i in (2,4)),1.1,55-i%4*3)
                if i in (1,4,7):
                    cue.note(10,section+beat+.20,pitch-12,1.48,44)
        cue.note(1,62.45,81,1.23,45)
    return cue
