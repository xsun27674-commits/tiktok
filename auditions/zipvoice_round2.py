"""Generate experimental Mandarin auditions without changing the studio voice preset."""
import argparse
import sys
from array import array
from pathlib import Path
from subprocess import run

import sherpa_onnx as sherpa

from studio.voice import AUDITION, Kokoro, VOICES

REFERENCE_TEXT = '哇，窗边的叶子动了一下！你看见了吗？我想凑近一点看看。'


def generate(model, vocoder, lexicon, reference_model, output, voices):
    output.mkdir(parents=True,exist_ok=True)
    ref_engine = Kokoro(reference_model)
    zip_model = sherpa.OfflineTtsZipvoiceModelConfig(
        tokens=str(model/'tokens.txt'),
        encoder=str(model/'encoder.int8.onnx'),
        decoder=str(model/'decoder.int8.onnx'),
        lexicon=f"{model/'lexicon.txt'},{lexicon}",
        vocoder=str(vocoder),
    )
    config = sherpa.OfflineTtsConfig(
        model=sherpa.OfflineTtsModelConfig(zipvoice=zip_model, num_threads=3, provider='cpu')
    )
    if not config.validate():
        raise ValueError('Invalid ZipVoice configuration')
    engine = sherpa.OfflineTts(config)
    passage = ''.join(AUDITION)
    for name in voices:
        print(f'Generating {name}',flush=True)
        reference = ref_engine.speak(REFERENCE_TEXT,name,1.)
        settings = sherpa.GenerationConfig()
        settings.reference_text = REFERENCE_TEXT
        settings.reference_audio = reference.samples
        settings.reference_sample_rate = reference.sample_rate
        settings.num_steps = 8
        settings.extra = {'min_char_in_sentence':'90'}
        clip = engine.generate(passage,settings)
        if len(clip.samples)<clip.sample_rate*4:
            raise RuntimeError(f'Incomplete synthesis for {name}')
        signal = array('f',clip.samples)
        if sys.byteorder!='little':
            signal.byteswap()
        run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(clip.sample_rate),
             '-ac','1','-i','pipe:0','-af','loudnorm=I=-19:TP=-2:LRA=11','-ar','24000',
             '-c:a','libmp3lame','-b:a','128k',str(output/f'zipvoice-{name}.mp3')],
            input=signal.tobytes(),check=True)


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--model',required=True,type=Path)
    cli.add_argument('--vocoder',required=True,type=Path)
    cli.add_argument('--lexicon',required=True,type=Path)
    cli.add_argument('--reference-model',required=True,type=Path)
    cli.add_argument('--output',type=Path,default=Path('output/voice-round2'))
    cli.add_argument('--voice',action='append',choices=VOICES)
    args=cli.parse_args()
    generate(args.model,args.vocoder,args.lexicon,args.reference_model,args.output,args.voice or VOICES)


if __name__=='__main__':
    main()
