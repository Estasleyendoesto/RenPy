#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: autocamFX
# version: 1.8
# description: Camera effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:

    class AutocamFX:
        def __init__(self, bg, speed = 0.001):
            # Background
            self.bg     = renpy.load_image( Image(bg) )
            self.bgsize = self.bg.get_size()

            self.x = 0
            self.y = 0

            self.dx = 0
            self.dy = 0

            self.speed = speed
        
        def draw(self, render, x, y):
            # true size of the box
            width, height = render.get_size()
            relw = (self.bgsize[0] - width) * x // width
            relh = (self.bgsize[1] - height) * y // height

            self.dx = relw - self.x
            self.dy = relh - self.y

            # travel speed
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))
        
        def meta(self):
            return (self.x, self.y, self.dx, self.dy)