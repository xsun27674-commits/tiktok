"""Export an episode by specifying the module that provides EPISODE."""
import argparse
from importlib import import_module
from pathlib import Path

from PIL import Image
from studio.graphics import paper_card
from studio.renderer import CAPTION_SCALE, Program, encode


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--episode',default='episodes.light_demo')
    cli.add_argument('--output',type=Path,default=Path('output/program-test.mp4'))
    audio=cli.add_mutually_exclusive_group()
    audio.add_argument('--demo-music',action='store_true')
    audio.add_argument('--music',type=Path)
    cli.add_argument('--previews',type=Path)
    args=cli.parse_args()
    module=import_module(args.episode)
    program=Program(module.EPISODE)
    encode(program,args.output,args.music,args.demo_music)
    if args.previews:
        args.previews.mkdir(parents=True,exist_ok=True)
        e=program.episode
        for label,beat in (('intro',2),('story',e.story_start+2),('summary',e.summary_start+2)):
            image=program.frame(float(program.clock.seconds(beat)),caption_scale=CAPTION_SCALE)
            image.resize((1280,720),Image.Resampling.NEAREST).save(args.previews/f'{label}.png')

        example=getattr(module,'PAPER_EXAMPLE',None)
        card=program.card if program.card is not None else paper_card(example) if example else None
        if card is not None:
            card.resize((960,540),Image.Resampling.NEAREST).save(args.previews/'paper-card.png')


if __name__=='__main__':
    main()
