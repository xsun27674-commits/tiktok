"""Reuse the show's stepped pixel curtain for either direction."""
from PIL import Image

from art import Canvas
from studio.graphics import curtain


def wipe(source, destination, progress, scale):
    layer = Canvas((source.width//scale, source.height//scale))
    curtain(layer, min(1,max(0,progress)))
    frame = (source if progress < .5 else destination).copy()
    frame.alpha_composite(layer.image.resize(frame.size, Image.Resampling.NEAREST))
    return frame
