#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: CamFX
# version: 1.0
# description: Camera effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:

    class CamFX:
        """
        La imagen del background debe ser de una resolución mayor a 1080p (según el juego, 2100p recomendado)
        Debido a las limitantes del juego, se recomienda jugar a pantalla completa (60fps, 30fps en modo ventana)
        Los atributos X e Y pueden definir la posición de otros objetos si se incluyen dentro del marco
        La velocidad de desplazamiento en flotante
        """

        def __init__(self, bg, speed = 0.01):
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
            width, height = render.get_size()
            # El ancho y alto relativo al fondo y la ventana según la posición del cursor
            relw = (self.bgsize[0] - width) * self.mouseX // width
            relh = (self.bgsize[1] - height) * self.mouseY // height

            # La diferencia entre el punto A y B
            self.dx = relw - self.x
            self.dy = relh - self.y

            # Velocidad relativa a la distancia (más lejos, más rápido; más cerca, más lento)
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            # Out of window fix
            if self.mouseX > 0 and self.mouseY > 0:
                self.oldx, self.oldy = self.x, self.y
            else:
                self.x, self.y = self.oldx, self.oldy

            # subsurface = recorte de la imagen de fondo
            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))


        def mouse(self, x, y):
            self.mouseX = x
            self.mouseY = y
        

        def meta(self):
            return (self.x, self.y, self.dx, self.dy, self.mouseX, self.mouseY)