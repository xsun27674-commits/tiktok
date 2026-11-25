"""Local Mandarin synthesis and a deterministic voice timing track."""
from dataclasses import dataclass
from pathlib import Path
from subprocess import run
import argparse
import json
import math
import wave
from array import array
import sys
from tempfile import TemporaryDirectory
from shutil import copyfile

AUDITION = (
    '咦？科学家为什么要修改一粒小麦的DNA呢？',
    '难道这和我们每天吃的面包有关？',
    '让我翻翻今天的科研笔记吧！',
)
# IDs follow the voice metadata in the pinned v1.1-zh ONNX artifact.
VOICES = {'zf_001':3, 'zf_005':7, 'zf_017':11,
          'zm_009':58, 'zm_012':61, 'zm_016':65}
RATE = 24
SPEED = 1.0


class Kokoro:
    def __init__(self, path):
        import sherpa_onnx as sherpa

        self.sherpa = sherpa
        path = Path(path)
        # Keep captions unchanged while adding a letter-by-letter lexicon entry.
        temporary = TemporaryDirectory()
        english = Path(temporary.name)/'lexicon-us-en.txt'
        copyfile(path/'lexicon-us-en.txt',english)
        with english.open('a',encoding='utf-8') as lex:
            lex.write('\nDNA d ˈ i ˈ ɛ n ˈ A\ndna d ˈ i ˈ ɛ n ˈ A\n')
        lexicon = f"{path/'lexicon-zh.txt'},{english}"

        rules = ','.join(str(path/f'{name}-zh.fst') for name in ('phone','date','number'))
        model = sherpa.OfflineTtsKokoroModelConfig(
            model=str(path/'model.int8.onnx'), voices=str(path/'voices.bin'),
            tokens=str(path/'tokens.txt'), lexicon=lexicon,
        )
        config = sherpa.OfflineTtsConfig(
            model=sherpa.OfflineTtsModelConfig(kokoro=model,num_threads=2,provider='cpu'),
            rule_fsts=rules,max_num_sentences=1,
        )
        if not config.validate():
            raise ValueError('Invalid Kokoro model directory')
        self.tts = sherpa.OfflineTts(config)
        temporary.cleanup()

    def speak(self, text, voice, speed):
        config = self.sherpa.GenerationConfig()
        config.sid = VOICES[voice]
        config.speed = speed
        config.silence_scale = .3
        return self.tts.generate(text, config)


@dataclass(frozen=True)
class SpokenCue:
    text: str
    expression: str = 'default'
    action: str = 'idle'
    pause_seconds: float = .18


def timestamp(seconds):
    ms = round(seconds*1000)
    minutes, ms = divmod(ms,60000)
    hours, minutes = divmod(minutes,60)
    seconds, ms = divmod(ms,1000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}'


def render_voice(engine, voice, cues, output, speed=SPEED):
    """Return audio, subtitle bounds and provisional mouth frames on one clock."""
    output = Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    samples = array('h')
    segments = []
    rate = engine.tts.sample_rate
    for cue in cues:
        audio = engine.speak(cue.text,voice,speed)
        if len(audio.samples)==0 or audio.sample_rate!=rate:
            raise RuntimeError(f'Unexpected TTS result for {cue.text}')
        start = len(samples)/rate
        samples.extend(round(max(-1,min(1,float(x)))*28000) for x in audio.samples)
        end = len(samples)/rate
        segments.append(dict(start=start,end=end,text=cue.text,
                             expression=cue.expression,action=cue.action))
        samples.extend([0]*round(cue.pause_seconds*rate))

    mouth = []
    for i in range(math.ceil(len(samples)*RATE/rate)):
        window = samples[round(i*rate/RATE):round((i+1)*rate/RATE)]
        level = math.sqrt(sum(x*x for x in window)/max(1,len(window)))
        mouth.append('closed' if level<200 else 'small' if level<2200 else 'open')
    timing = dict(voice=voice, speed=speed, sample_rate=rate,
                  fps=RATE, segments=segments, mouth_frames=mouth)

    if sys.byteorder!='little':
        samples.byteswap()
    with wave.open(str(output.with_suffix('.wav')),'wb') as audio:
        audio.setparams((1,2,rate,0,'NONE','not compressed'))
        audio.writeframes(samples.tobytes())
    output.with_suffix('.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2)+'\n',
                                           encoding='utf-8')
    captions = [
        f"{i}\n{timestamp(segment['start'])} --> {timestamp(segment['end'])}\n{segment['text']}\n"
        for i,segment in enumerate(segments,1)
    ]
    output.with_suffix('.srt').write_text('\n'.join(captions),encoding='utf-8')
    return timing


def speech_at(timing, seconds):
    """Return a line and provisional mouth shape at the supplied clip time."""
    index = math.floor(seconds*timing['fps'])
    mouth = timing['mouth_frames']
    if not 0<=index<len(mouth):
        return None, 'closed'
    cue = next((segment for segment in timing['segments']
                if segment['start']<=seconds<segment['end']), None)
    return cue, mouth[index] if cue else 'closed'


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--model',type=Path,required=True)
    cli.add_argument('--output',type=Path,default=Path('output/voice-auditions'))
    cli.add_argument('--voice',choices=VOICES,action='append')
    cli.add_argument('--speed',type=float,default=SPEED)
    args = cli.parse_args()
    if args.speed<=0:
        cli.error('--speed must be positive')
    engine = Kokoro(args.model)
    cues = [SpokenCue(line,expression,action) for line,expression,action in zip(
        AUDITION,('confused','inspired','focused'),('think','idle','read')
    )]
    for voice in args.voice or VOICES:
        path = args.output/voice
        render_voice(engine,voice,cues,path,args.speed)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path.with_suffix('.wav')),
             '-c:a','libmp3lame','-b:a','96k',str(path.with_suffix('.mp3'))],check=True)


if __name__=='__main__':
    main()
