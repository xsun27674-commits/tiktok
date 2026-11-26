"""Render a branded edition of any compatible studio episode."""
import argparse
from dataclasses import replace
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from studio.brand import archive, sound
from studio.brand import music
from studio.brand.program import BrandProgram
from studio.renderer import CAPTION_SCALE, encode
from studio.timeline import Cue
from studio.papermark import PaperMark, REFLECTION_SECONDS


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--episode',default='episodes.light_demo')
    cli.add_argument('--number',type=int,required=True)
    cli.add_argument('--theme',help='Override the archive theme; defaults to episode title')
    cli.add_argument('--catalog',type=Path,default=Path('assets/brand/archive-catalog.json'))
    cli.add_argument('--output',type=Path,default=Path('output/brand-test.mp4'))
    cli.add_argument('--previews',type=Path)
    cli.add_argument('--sounds',type=Path,help='Export the individual sound cues as WAV')
    cli.add_argument('--record',action='store_true',help='Record the archive after successful encoding')
    cli.add_argument('--compact-demo',action='store_true',help='Use the short light-demo story fixture')
    cli.add_argument("--story-music", choices=("adventure","micro"), default="adventure")
    cli.add_argument("--effects-only", action="store_true", help="Reproduce the original effects-only demo")
    cli.add_argument("--check", action="store_true", help="Validate timeline and audio without exporting video")
    cli.add_argument("--paper-mark", type=Path, help="PaperMark evidence and rights manifest")
    args=cli.parse_args()
    e=import_module(args.episode).EPISODE
    if args.compact_demo:
        if args.episode!='episodes.light_demo':
            cli.error('--compact-demo applies to episodes.light_demo')
        e=replace(e,intro=(Cue(0,'一片小小的叶子，能从阳光里得到什么？','confused','think'),),
                  story=(Cue(6,'叶绿素能吸收光。','focused'),
                         Cue(11,'叶片利用光能，把能量储存在糖里。','excited')),
                  summary=(Cue(19,'植物把光能转成化学能，\n把能量储存在糖里。','focused'),),
                  story_start=6,summary_start=19,end=25)
    paper_mark=PaperMark(args.paper_mark) if args.paper_mark else None
    doi=paper_mark.info['doi'] if paper_mark else (e.paper.doi if e.paper else '')
    if paper_mark and e.paper and e.paper.doi!=doi:
        cli.error('PaperMark manifest and episode DOI differ')
    entry=archive.Archive(args.number,args.theme or e.title,doi)
    program=BrandProgram(e,entry,archive.load(args.catalog),paper_mark=paper_mark)
    with TemporaryDirectory() as tmp:
        track=Path(tmp)/'brand.wav'
        program.write_audio(track)
        if not args.effects_only:
            mixed=Path(tmp)/"mixed.wav"
            music.mix(program,track,mixed,args.story_music)
            track=mixed
        if args.check:
            points=program.edges[:-1]
            if paper_mark:
                points += [program.edges[1]+t for t in (1.8,7)]
                points += [program.edges[3]+f.start+.001 for f in paper_mark.figures]
                points += [program.edges[5]+program.summary_seconds+t
                           for t in (.1,REFLECTION_SECONDS/2+.1)]
            for point in points:
                program.frame(point+0.0001,caption_scale=CAPTION_SCALE)
            print(f"Validated {entry.code}, {program.total_frames} frames and audio mix; no video exported")
            return
        encode(program,args.output,music=track)
    if args.previews:
        args.previews.mkdir(parents=True,exist_ok=True)
        times={'opening':1.58,'transition':program.edges[2]+.31,'story':program.edges[3]+.6,
               'stamp':program.edges[6]+2.7,'shelf':program.edges[6]+4.7,
               'ending':program.edges[6]+9.6}
        for name,t in times.items():
            frame=program.frame(t,caption_scale=CAPTION_SCALE)
            frame.resize((1280,720),Image.Resampling.NEAREST).save(args.previews/f'{name}.png')
    if args.sounds:
        args.sounds.mkdir(parents=True,exist_ok=True)
        for cue,notes in sound.CUES.items():
            duration=max(offset+length for offset,_,length in notes)+.06
            sound.write(args.sounds/f'{cue}.wav',duration,((.015,cue),))
    if args.record:
        archive.save(args.catalog,entry)


if __name__=='__main__':
    main()
