#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: ParallaxFX
# version: 2.3
# description: Parallax Effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    class Layer:
        """
        It is important for Parallaxfx to function properly.
        """

        def __init__(self, bg, delay=0.00):
            self.delay = delay
            self.bg    = bg
            # aux
            self.oldx = 0
            self.oldy = 0


    class Parallaxfx:
        """
        If last layer is "unstable" or "vibrates", delay 0.0 to correct it.
        Important to define the displacement speed for each layer.
        You can select to apply the effect on x-axis, y-axis or both together.
        Different speed could be defined for x and y (in development)

        Constructor receives as parameters:
            - Camfx object (required)

        Add method receives as parameters:
            - bg = '*.png|jpeg|webp'
            - delay = 0.00 (0 = same speed as camera)
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

        def draw(self, render):
            width, height = render.get_size()
            x, y, dx, dy, mouseX, mouseY = self.camfx.meta

            for layer in self.layers:
                # custom speed
                if self.x_on:
                    x += dx * layer.delay
                if self.y_on:
                    y += dy * layer.delay

                # out of box fix
                if mouseX > 0 and mouseY > 0:
                    layer.oldx, layer.oldy = x, y
                else:
                    x, y = layer.oldx, layer.oldy
 
                # progresive loader
                layer.bg = self.optimize(layer.bg)
                # cut and draw
                bg = layer.bg.subsurface( (x, y, width, height) )
                render.blit(bg, (0, 0))

        def add(self, *layer):
            self.layers.append( Layer(*layer) )