# name: GIFtoFile
# version: 1.3
# description: Image sequence packaging to cpickle
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

import sys
import os
import io

def compile(input, ext='webp'):
    """
    input = Nombre de la animación (gif, png, webp)
    ext = Extensión de los frames (gif, webp, png, jpeg)(webp por defecto)
    """

    output = os.path.splitext(input)[0] + '.res'

    try:
        # Python <= 2.7
        import cPickle
    except:
        # pickle incluye acelerador en C para python 3+
        import pickle as cPickle

    try:
        from PIL import Image, ImageSequence
    except:
        print('PIL no está instalado en su dispositivo')

    import base64

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
        file = str(i) + '.' + ext
        try:
            if ext == 'webp':
                frame.save( file, format=formats[ext], lossless=False )
            else:
                frame.save( file, format=formats[ext], optimize=True )
        except:
            print(ext, 'no es un formato soportado')
            print('Formatos soportados: webp, jpeg, png, gif')
            return None

        # Conversión a base 64
        img = open( file, 'rb' ).read()
        b64 = base64.b64encode(img)
        # Corrección de los paddíngs
        b64  = b64.decode('utf-8')
        data = b64.replace('=', '')
        data += '=' * (-len(data) % 4)
        # Almacenado
        frames.append( data )
        # Borrado en disco
        os.remove(file)
        i += 1

    # Guardarlos con cPickle
    with open(output, 'wb') as fp:
        cPickle.dump(frames, fp, protocol=2)

    print('Compilación completada')

#   ......
#   ......
if len(sys.argv) == 2:
    compile( sys.argv[1] )

elif len(sys.argv) == 3:
    compile( sys.argv[1], sys.argv[2] )

else:
    print('Necesita al menos la entrada del fichero')

