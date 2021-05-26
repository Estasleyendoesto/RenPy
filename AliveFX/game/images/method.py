# name: GIFtoFile
# version: 1.0
# description: Image sequence to cpickle tuple
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

# pickle incluye acelerador en C para python 3
try:
    import cPickle
except:
    import pickle as cPickle

from PIL import Image, ImageSequence

"""
# Extraer los frames del gif
im = Image.open("nigga.gif")
i = 0
for frame in ImageSequence.Iterator(im):
    i += 1
    frame.save( str(i) + '.webp', format='WebP', lossless=True )
"""

# Guardarlos con cPickle

