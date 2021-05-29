import numpy as np
import pickle
import cv2
import sys
import os

def compile(input):
    """
    Script que convierte una imagen con transparencia en una máscara (*.dat)
    Tengo pensado implementar un algoritmo de compresión (si renpy permite el uso de threads)
    input = *.png (transparencia)
    """

    # Obtenemos la máscara de una imagen con transparencia
    img = cv2.imread(input, cv2.IMREAD_UNCHANGED)
    alpha = img[:, :, 3]
    alpha = cv2.threshold(alpha, 0, 1, cv2.THRESH_BINARY)[1]

    # Array al que pasaremos a limpio
    clean = []
    for i in range(0, len(alpha)):
        list = []
        for a in alpha[i]:
            # Convertimos a integer para ahorrar aun más espacio
            list.append(int(a)) 
        # Convertimos a tupla (ahorrar espacio y recursos)
        list = tuple(list)    
        clean.append(list)

    # Convertimos la lista principal en tupla
    clean = tuple(clean)

    # Almacenamos en un fichero
    output = os.path.splitext(input)[0] + '.dat'
    with open(output, 'wb') as fp:
        pickle.dump(clean, fp, protocol=2)

#   ......
#   ......
if len(sys.argv) == 2:
    compile( sys.argv[1] )
else:
    print('Necesita la entrada del fichero')