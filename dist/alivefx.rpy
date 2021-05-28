#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: AliveFX
# version: 2.3
# description: Image sequence player for Ren'Py Engine (frametool.py is necesary)
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

# PLANES A FUTURO:
# sleep()       -> Tiempo de reposo entre cada ciclo de vida de una animación (principio a fin)
# composer()    -> Programar cómo se comportará cada frame o grupo de frames (delay, sleep, loop, rever)
# Nota: Quizás sea más eficiente programar el comportamiento desde un .json e interpretarlo aquí.

init python:
    import cPickle
    import pygame
    import base64
    import math
    import io
    
    class AliveFX:
        """
        AliveFX es una herramienta para el desplegado de secuencias de imágenes.
        Puede usarse en su propio displayable o junto a CamFX con sus funcionalidades.
        Activando landscape puede usarse en modo fondo animado.
        El constructor puede recibir lo siguiente:
            - res = '*.res' (requerido)
            - delay = 0.000
            - loop = 0
            - rever = False
            - landscape = False
        """

        def __init__(self, res, delay=0.0, loop=0, rever=False, landscape=False):
            file = renpy.file(res).name 
            # ...
            res  = cPickle.load( open(file, 'rb') )
            self.frames = [ io.BytesIO(base64.b64decode( frame )) for frame in res ]

            self.loop  = loop  # 0 = inf
            self.delay = delay # millis (per frame, 0.001 -> 1.0)
            self.rever = rever # zigzag animation
            
            # experimental
            self.landscape = landscape

            # aux
            self.pos   = 0
            self.sec   = 0.0
            self.times = 0
            self.delta = 0
            
        def on(self, render, st, x, y):
            if self.sleeper(st):
                if self.looper():
                    self.tracker()
            
            frame = self.optimize()

            # Experimental
            if self.landscape:
                width, height = render.get_size()
                frame = frame.subsurface( (x, y, width, height) )
                x, y = 0, 0

            # Esto no xD
            render.blit( frame, (x, y) )

        def tracker(self):
            if self.rever:
                if self.pos == 0 : self.delta = 1
                if self.pos == len(self.frames) - 1 : self.delta = -1
                self.pos += self.delta
            else:
                self.pos += 1 if self.pos < len(self.frames) - 1 else -self.pos

        def looper(self):
            if self.loop:
                if self.times < self.loop + 1:  # Little cheat
                    if not self.pos:
                        self.times += 1
                else:
                    return False
                    
            return True

        def sleeper(self, st):
            duration = self.delay
            duration = 0.001 if not duration else duration

            t = duration * 1000
            v = len(self.frames) / t
            d = st / v

            if math.modf(d)[1] > self.sec:
                self.sec = d
                return True

        def optimize(self):
            frame = self.frames[self.pos]

            if isinstance(frame, io.BytesIO):
                frame = pygame.image.load(frame)
                self.frames[self.pos] = frame

            return frame

        def sleeperOLD(self):
            self.sec += 0.1
            if self.sec > self.delay:
                self.sec -= self.sec
                return True