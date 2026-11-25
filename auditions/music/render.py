"""Render the original audition arrangements with a user-supplied SoundFont."""
import argparse
import json
import ctypes as C
from ctypes.util import find_library
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import wave

import numpy as np

from .score import LEVELS, PAN, PATCHES, compose

RATE = 44100


def bind():
    lib=C.CDLL(find_library('fluidsynth') or 'libfluidsynth.so.3')
    ptr,integer,text=C.c_void_p,C.c_int,C.c_char_p
    signatures={
        'new_fluid_settings':(ptr,()),'delete_fluid_settings':(None,(ptr,)),
        'fluid_settings_setnum':(integer,(ptr,text,C.c_double)),
        'new_fluid_synth':(ptr,(ptr,)),'delete_fluid_synth':(None,(ptr,)),
        'fluid_synth_sfload':(integer,(ptr,text,integer)),
        'fluid_synth_program_select':(integer,(ptr,integer,integer,integer,integer)),
        'fluid_synth_cc':(integer,(ptr,integer,integer,integer)),
        'fluid_synth_noteon':(integer,(ptr,integer,integer,integer)),
        'fluid_synth_noteoff':(integer,(ptr,integer,integer)),
        'fluid_synth_write_float':(integer,(ptr,integer,ptr,integer,integer,ptr,integer,integer)),
    }
    for name,(result,args) in signatures.items():
        entry=getattr(lib,name)
        entry.restype=result
        entry.argtypes=args
    return lib


def render(cue,soundfont,output):
    lib=bind()
    settings=lib.new_fluid_settings()
    for key,value in ((b'synth.sample-rate',RATE),(b'synth.gain',.65),
                      (b'synth.reverb.level',.26),(b'synth.reverb.room-size',.43)):
        lib.fluid_settings_setnum(settings,key,value)
    synth=lib.new_fluid_synth(settings)
    try:
        bank=lib.fluid_synth_sfload(synth,str(soundfont).encode(),1)
        if bank<0:
            raise RuntimeError('SoundFont could not be loaded')
        for index,(patch,pan,level) in enumerate(zip(PATCHES,PAN,LEVELS)):
            channel=index if index<9 else index+1  # GM channel ten is reserved for percussion.
            if lib.fluid_synth_program_select(synth,channel,bank,0,patch):
                raise RuntimeError(f'Could not select GM patch {patch}')
            for controller,value in ((10,pan),(7,level),(91,65),(93,5)):
                lib.fluid_synth_cc(synth,channel,controller,value)
        frames=round((64*60/cue.bpm+2.1)*RATE)
        signal=np.zeros((frames,2),dtype=np.float32)
        previous=0
        silence=(frames,0,0,0)
        events=[(round(beat*60*RATE/cue.bpm),ch,note,velocity)
                for beat,ch,note,velocity in cue.events]
        for frame,ch,note,velocity in sorted(events)+[silence]:
            if frame>previous:
                buf=signal[previous:frame]
                ptr=buf.ctypes.data
                if lib.fluid_synth_write_float(synth,len(buf),ptr,0,2,ptr,1,2):
                    raise RuntimeError('FluidSynth rendering failed')
                previous=frame
            if frame==frames:
                break
            if velocity:
                lib.fluid_synth_noteon(synth,ch,note,velocity)
            else:
                lib.fluid_synth_noteoff(synth,ch,note)
        tail=round(.40*RATE)
        signal[-tail:]*=np.linspace(1,0,tail,dtype=np.float32)[:,None]
        peak=np.max(np.abs(signal))
        if peak<.01:
            raise RuntimeError('Silent rendition')
        signal*=.82/peak
        with TemporaryDirectory() as tmp:
            raw=Path(tmp)/'cue.wav'
            with wave.open(str(raw),'wb') as wav:
                wav.setparams((2,2,RATE,0,'NONE','not compressed'))
                wav.writeframes((signal*32767).astype('<i2').tobytes())
            measurement=run(['ffmpeg','-hide_banner','-i',str(raw),'-af',
                             'loudnorm=print_format=json','-f','null','-'],
                            capture_output=True,text=True,check=True).stderr
            analysis,_=json.JSONDecoder().raw_decode(measurement[measurement.rfind('{'):])
            gain=min(-17-float(analysis['input_i']),-1.6-float(analysis['input_tp']))
            run(['ffmpeg','-v','error','-y','-i',str(raw),'-af',f'volume={gain:.2f}dB',
                 '-c:a','libmp3lame','-q:a','2',str(output)],check=True)
    finally:
        lib.delete_fluid_synth(synth)
        lib.delete_fluid_settings(settings)


if __name__=='__main__':
    cli=argparse.ArgumentParser()
    cli.add_argument('--soundfont',required=True,type=Path)
    cli.add_argument('--output',type=Path,default=Path('output/music-auditions'))
    args=cli.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    for style in range(4):
        cue=compose(style)
        render(cue,args.soundfont,args.output/f'{cue.name}.mp3')
