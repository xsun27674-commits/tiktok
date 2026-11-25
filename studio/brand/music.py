"""Mix the four approved V1.0 arrangements with the fixed brand sound cues."""
from pathlib import Path
from subprocess import run
from studio.renderer import FPS

TRACKS = {
    'cabin': '01-research-cabin.mp3',
    'adventure': '02-science-adventure.mp3',
    'micro': '03-microworld.mp3',
    'discovery': '04-todays-discovery.mp3',
}
LIBRARY = Path(__file__).resolve().parents[2] / 'output' / 'music-auditions'


def mix(program, effects, destination, story):
    sections = (
        ('cabin', 0, program.edges[3], .16),
        (story, program.edges[3], program.edges[5], .16),
        ('discovery', program.edges[5], program.total_frames/FPS, .13),
    )
    args = ['ffmpeg', '-v', 'error', '-y', '-i', str(effects)]
    filters = []
    for index, (track, start, end, gain) in enumerate(sections, 1):
        args += ['-stream_loop', '-1', '-i', str(LIBRARY / TRACKS[track])]
        length = end-start
        fade = min(.65, length/3)
        filters.append(
            f'[{index}:a]atrim=duration={length:.6f},asetpts=PTS-STARTPTS,'
            f'volume={gain},afade=d={fade:.6f},'
            f'afade=t=out:st={length-fade:.6f}:d={fade:.6f},'
            f'adelay={round(start*1000)}:all=1[m{index}]'
        )
    filters.append('[0:a][m1][m2][m3]amix=inputs=4:normalize=0:duration=first[out]')
    run(args + ['-filter_complex', ';'.join(filters), '-map', '[out]',
                '-ar', '24000', '-ac', '2', str(destination)], check=True)
