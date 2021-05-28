#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: ParallaxFX
# version: 2.1
# description: Parallax Effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    class Layer:
        """
        Es importante para el funcionamiento de ParallaxFX
        """

        def __init__(self, bg, delay=0.00):
            self.delay = delay
            self.bg    = bg
            # aux
            self.oldx = 0
            self.oldy = 0


    class ParallaxFX:
        """
        Si la última capa es "inestable" o "vibra", delay a 0.0 para corregirlo
        Es importante definir la velocidad de desplazamiento para cada layer
        Puede seleccionar aplicar el efecto en el eje x, y, o ambos juntos
        Podría definirse una velocidad distinta para x e y (en desarrollo)

        Constructor recibe como parámetros:
            - CamFX object (requerido)

        El método add recibe como parámetros:
            - bg    = '*.png|jpeg'
            - delay = 0.00 (0 = misma velocidad que la cámara)
        """

        def __init__(self, camfx):
            self.camfx = camfx
            self.layers = []
            # Enable x, y axis
            self.x_on = True
            self.y_on = False

        def optimize(self, bg):
            if isinstance(bg, str):
                return renpy.load_image( Image(bg) )
            return bg

        def on(self, render):
            width, height = render.get_size()
            x, y, dx, dy, mouseX, mouseY = self.camfx.meta()

            for layer in self.layers:
                if self.x_on:
                    x += dx * layer.delay
                if self.y_on:
                    y += dy * layer.delay

                # out of box fix
                if mouseX > 0 and mouseY > 0:
                    layer.oldx, layer.oldy = x, y
                else:
                    x, y = layer.oldx, layer.oldy
 
                bg = self.optimize(layer.bg).subsurface( (x, y, width, height) )
                render.blit(bg, (0, 0))


        def add(self, bg, delay = 0):
            self.layers.append( Layer(bg, delay) )