#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: CamFX
# version: 1.8
# description: Camera effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:

    class CamFX:
        """
        Simulador de efecto cámara basado en Creator-Defined Displayables
        El constructor recibe lo siguiente:
            - bg    = '*.png|jpeg|webp' (requerido)
            - speed = 0.000 (velocidad de desplazamiento)

        El método meta devuelve lo necesario para sus propias integraciones
        *efecto Dissolve para transición no se aconseja su uso
        """

        def __init__(self, bg, speed = 0.001):
            # Background
            self.bg     = renpy.load_image( Image(bg) )
            self.bgsize = self.bg.get_size()

            self.x = self.bgsize[0] // 4
            self.y = self.bgsize[1] // 4

            self.oldx = 0
            self.oldy = 0

            self.dx = 0
            self.dy = 0

            self.mouseX = 0
            self.mouseY = 0

            self.speed = speed
        
        def fx_on(self, render):
            # true size of the box
            width, height = render.get_size()
            relw = (self.bgsize[0] - width) * self.mouseX // width
            relh = (self.bgsize[1] - height) * self.mouseY // height

            self.dx = relw - self.x
            self.dy = relh - self.y

            # travel speed
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            # out of box fix
            if self.mouseX > 0 and self.mouseY > 0:
                self.oldx, self.oldy = self.x, self.y
            else:
                self.x, self.y = self.oldx, self.oldy

            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))

        def mouse(self, x, y):
            self.mouseX = x
            self.mouseY = y
        
        def meta(self):
            return (self.x, self.y, self.dx, self.dy, self.mouseX, self.mouseY)