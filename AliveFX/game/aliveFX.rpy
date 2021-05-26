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
    import io
    import gc
    
    class AliveFX:
        def __init__(self, res, loop=0, speed=0.00, rever=False):
            self.loop  = loop  # 0 = inf
            self.speed = speed # millis (per frame)
            self.rever = rever # Animación reversa

            # Open package of frames
            file = renpy.file(res).name

            gc.disable()
            res  = cPickle.load( open(file, 'rb') )
            gc.enable()

            frames = []

            for frame in res:
                decode = io.BytesIO(base64.b64decode( frame ))
                frames.append( pygame.image.load(decode) )

            self.frames = tuple(frames)


        def on(self, render):
            render.blit( self.frames[0], (0, 0) )