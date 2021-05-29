# name: GIFtoFile
# version: 3.4
# description: Image sequence to cpickle tuple
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

from PIL import Image, ImageSequence
import pickle as cPickle
import numpy as np
import base64
import sys
import os


# Extracción del color dominante para la correción de gifs corruptos (parcial)
def get_dominant_color(im):
    img = im.copy()
    img.convert('RGB')
    img.resize( (1,1), resample=0 )
    index = img.getpixel( (0,0) )
    return index
    """
    # palette = img.getpalette()
    base = 3 * index
    r, g, b = palette[base:base+3]
    return (r, g, b)
    """
    
# Compilador individual a base 64
def compile(files, output):
    # Extraer los frames del gif y guardarlos en una lista
    frames = []

    for file in files:
        # Conversión a base 64
        img = open( file, 'rb' ).read()
        b64 = base64.b64encode(img)

        # Corrección de los paddíngs
        b64  = b64.decode('utf-8')
        data = b64.replace('=', '')
        data += '=' * (-len(data) % 4)

        # Almacenado
        frames.append( data )

        # Borrado en memoria
        os.remove(file)

    # Compilado...
    with open(output, 'wb') as fp:
        cPickle.dump(frames, fp, protocol=2)

    print('Compilación completada')


# Por el momento este algoritmo funciona mejor
def most_frequent_colour(image):
    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            # Evitar transparencias
            if colour != (0, 0, 0, 0):
                most_frequent_pixel = (count, colour)

    return most_frequent_pixel

# Limpia imágenes corruptas
def recleaner(files, repeat=1):
    for r in range(0, repeat):
        for file in files:
            im = Image.open(file)
            # dominant_color = get_dominant_color(im)
            # dominant_color = ColorThief(file).get_color(quality=1)
            # print(dominant_color[1])
            dominant_color = most_frequent_colour(im)[1]
            
            alpha = (0, 0, 0, 0)
            
            # Reemplaza el color molesto por alpha
            pixdata = im.load() 
            for y in range(im.size[1]):
                for x in range(im.size[0]):
                    if pixdata[x, y] == dominant_color:
                        pixdata[x, y] = alpha

            # El último recorrido con compresión
            if r == repeat-1:
                im.save( file, format='WEBP', lossless=False)
            else:
                im.save( file, format='WEBP', lossless=True)


# Extractor de gifs a imágenes individuales
def extract(input, ext='webp', resolve=None, repeat=0):
    """
    input = Nombre de la animación (gif, png, webp)
    ext = Extensión de los frames (gif, webp, png)(webp por defecto)
    """

    formats = {
        'webp': 'WebP',
        #'jpeg': 'JPEG',
        'png' : 'PNG',
        'gif' : 'GIF'
    }

    # Extractor de secuencias de imágenes
    files = []
    i = 0
    im = Image.open(input)
    for frame in range(0, im.n_frames):
        im.seek( frame )
        file = str(i) + '.' + ext
        i += 1

        try:
            if ext == 'webp':
                im.save( file, format=formats[ext], lossless=True)
            else:
                im.save( file, format=formats[ext], optimize=True)
        except:
            print(ext, 'no es un formato soportado')
            print('Formatos soportados: webp, png, gif')
            return None

        files.append(file)

    # Filtro de colores molestos
    if resolve:
        recleaner(files, repeat)

    # Listo para compilar
    output = os.path.splitext(input)[0] + '.res'
    return files, output
    

# Enpaquetador
def packres(*args):
    if len(args) == 1:
        f, out = extract(*args)
    
    if len(args) == 2:
        if args[1] in ('-r', '--resolve'):
            f, out = extract( args[0], resolve=args[1] )
        else:
            f, out = extract( args[0], ext=args[1] )

    if len(args) == 3:
        if args[1] in ('-r', '--resolve'):
            repeats = int( ''.join(filter(str.isdigit, args[2])) )
            f, out = extract( args[0], resolve=args[1], repeat=repeats )
        else:
            f, out = extract( args[0], ext=args[1], resolve=args[2] )

    if len(args) == 4:
        repeats = int( ''.join(filter(str.isdigit, args[3])) )
        f, out = extract( args[0], ext=args[1], resolve=args[2], repeat=repeats )

    compile(f, out)


# Extracción de parámetros de consola
if len(sys.argv) > 1:
    packres(*sys.argv[1:])
elif len(sys.argv) > 4:
    print('Número de instrucciones no válido')
else:
    print('Necesita al menos la entrada del fichero')