#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: AliveFX
# version: 1.0
# description: Image sequence for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    import cPickle
    import pygame
    import base64
    import math
    import io

    import time
    
    class AliveFX:
        def __init__(self, res, delay=0.0, loop=0, rever=False):
            # Open package of frames
            file = renpy.file(res).name # Tarda en abrir (necesita optimzar)
            res  = cPickle.load( open(file, 'rb') )

            # frames = []
            # for frame in res:
                # byte = io.BytesIO(base64.b64decode( frame ))
                # print( decode.__class__.__name__ )
                # frames.append( byte )
                # start = time.time()
                # frames.append( pygame.image.load(decode) )
                # print( frames[-1].__class__.__name__ )
                # end = time.time()
                # print(end - start)

            # self.frames = frames
            self.frames = res

            self.loop  = loop  # 0 = inf
            self.delay = delay # millis (per frame, 0.001 -> 1.0)
            self.rever = rever # Animación reversa
            
            # Experimental
            self.landscape = False

            # Auxiliares
            self.pos   = 0
            self.sec   = 0.0
            self.times = 0
            self.delta = 0

        def optimize(self):
            frame = self.frames[self.pos]
            if frame.__class__.__name__ != 'Surface':
                byte = io.BytesIO(base64.b64decode( frame ))
                self.frames[0] = pygame.image.load(byte)

            # frame = self.frames[0]

            print(self.frames[0])
            # print(frame)
            # print(self.frames.index( frame ))
            print('---')
            # if frame.__class__.__name__ == 'BytesIO':
                # frame = pygame.image.load(frame)


            # print(frame)
            return frame

            # try:
                # frame = pygame.image.load(frame)
            # except:
                # pass

            # return frame
            

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


        # Recorrido normal o reverso
        def tracker(self):
            if self.rever:
                if self.pos == 0 : self.delta = 1
                if self.pos == len(self.frames) - 1 : self.delta = -1

                self.pos += self.delta
            
            else:
                self.pos += 1 if self.pos < len(self.frames) - 1 else -self.pos


        # Máximo número de recorridos
        def looper(self):
            if self.loop:
                if self.times < self.loop + 1:  # Little cheat
                    if not self.pos:
                        self.times += 1
                else:
                    return False
                    
            return True


        # Retraso para cada fotograma (variable)
        def sleeper(self, st):
            duration = self.delay
            duration = 0.001 if not duration else duration

            t = duration * 1000
            v = len(self.frames) / t
            d = st / v

            if math.modf(d)[1] > self.sec:
                self.sec = d
                return True


        # Retraso para cada fotograma (básica)
        def sleeperOLD(self):
            self.sec += 0.1
            if self.sec > self.delay:
                self.sec -= self.sec
                return True