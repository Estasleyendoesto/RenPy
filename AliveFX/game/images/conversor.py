# name: GIFtoFile
# version: 1.0
# description: Image sequence to cpickle tuple
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy



# Nombre de la animación (gif, png, webp)
# Formato de salida (xz)
# Extensión de los frames (gif, webp, png, jpeg)
input = 'nigga.gif'
output = 'nigga.res'
ext = 'webp'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
try:
    # Para Python < 2.7
    import cPickle
except:
    # pickle incluye acelerador en C para python 3+
    import pickle as cPickle

from PIL import Image, ImageSequence
import base64
import lzma
import os


# Extraer los frames del gif y guardarlos en una lista
frames = []
i = 0

formats = {
    'webp': 'WebP',
    'jpeg': 'JPEG',
    'png' : 'PNG',
    'gif' : 'GIF'
}

im = Image.open(input)
for frame in ImageSequence.Iterator(im):
    # Extracción de los frames y conversión de formato
    file = str(i) + '.' + ext
    frame.save( file, format=formats[ext], lossless=True )

    # Conversión a base 64
    img = open( file, 'rb' ).read()
    b64 = base64.b64encode(img)

    # Corrección de los paddíngs
    b64  = b64.decode('utf-8')
    data = b64.replace('=', '')
    data += '=' * (-len(data) % 4)
    
    # Almacenado
    frames.append( data )

    # Borrado en físico
    os.remove(file)
    i += 1

# Conversión a tupla
frames = tuple(frames)

# Guardarlos con cPickle
with open(output, 'wb') as fp:
    cPickle.dump(frames, fp, protocol=2)
