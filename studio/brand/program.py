"""Compose brand rituals around an existing three-part Program."""
from bisect import bisect_right
from pathlib import Path

from art import Canvas
from studio.brand import archive, ritual, sound, transition
from studio.renderer import FPS, Program


class BrandProgram:
    def __init__(self,episode,entry,records=()):
        self.base=Program(episode)
        self.entry=entry
        known=archive.collect(records,entry)
        self.prior=tuple(row for row in known if row.number<entry.number)
        self.collected=archive.collect(self.prior,entry)
        room=Canvas(self.base.room.size)
        room.paste(self.base.room,0,0)
        archive.shelf(room,self.prior)
        self.base.room=room.image
        self.intro=float(self.base.clock.seconds(episode.story_start))
        self.story_end=float(self.base.clock.seconds(episode.summary_start))
        self.end=float(self.base.clock.seconds(episode.farewell_start or episode.end))
        # Optional paper credits remain before the branded archive ritual.
        durations=(ritual.OPENING,self.intro,ritual.PORTAL,self.story_end-self.intro,
                   ritual.RETURN,self.end-self.story_end,ritual.ENDING)
        self.edges=[0.]
        for span in durations:
            self.edges.append(self.edges[-1]+span)
        self.total_frames=round(self.edges[-1]*FPS)

    def frame(self,seconds,caption_scale=1):
        part=min(6,bisect_right(self.edges,seconds)-1)
        local=seconds-self.edges[part]
        room=self.base.room
        scale=caption_scale
        if part==0:
            return ritual.opening(room,local,self.entry,scale)
        if part==1:
            return self.base.frame(local,scale,transitions=False)
        if part==2:
            source=self.base.frame(max(0,self.intro-1/FPS),scale,transitions=False)
            story=self.base.frame(self.intro,scale,transitions=False)
            return transition.wipe(source,story,local/ritual.PORTAL,scale)
        if part==3:
            return self.base.frame(self.intro+local,scale,transitions=False)
        if part==4:
            source=self.base.frame(self.story_end-1/FPS,scale,transitions=False)
            dest=self.base.frame(self.story_end,scale,transitions=False)
            progress=local/ritual.RETURN
            return transition.wipe(source,dest,progress,scale)
        if part==5:
            return self.base.frame(self.story_end+local,scale,transitions=False)
        return ritual.ending(room,local,self.prior,self.collected,self.entry,scale)

    def write_audio(self,path: Path):
        effects=((.02,'paper'),(1.67,'opening'),(self.edges[2]+.12,'sprout'),
                 (self.edges[3]+1.6,'discovery'),(self.edges[6]+2.05,'stamp'),
                 (self.edges[6]+8.9,'ending'))
        sound.write(path,self.total_frames/FPS,effects)
