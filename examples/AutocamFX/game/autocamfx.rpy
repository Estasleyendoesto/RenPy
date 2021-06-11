#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: autocamFX
# version: 1.8
# description: Camera effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    import random
    import math

    class AutocamFX:
        """
        Auto Camera effect simulator based on Creator-Defined Displayables
        The constructor receives the following:
            - bg = '*.png|jpeg|webp' or '1280x720' (required)
            - speed = 0.000 (scroll speed)
            - delay = 1000 == 1 second

        The meta method returns what is required for its own integrations.
        *Dissolve effect for transition not recommended
        """

        def __init__(self, bg, speed = 0.001, delay = 50):
            if os.path.splitext(bg)[1]:
                res = renpy.displayable(bg)
            else:
                i = list(bg).index('x')
                w, h = int(bg[:i]), int(bg[i+1:])
                solid = Solid((0,0,0, 0), xsize=w, ysize=h)
                res = renpy.displayable(solid)

            # Background
            self.bg     = res
            self.bgsize = None

            self.x = 0
            self.y = 0

            self.dx = 0
            self.dy = 0

            self.rx = 0
            self.ry = 0

            self.delay = delay

            self.speed = speed
            self.sec = 0

        def sleep(self, st):
            t = self.delay
            v = 24 / float(t)
            d = st / v
            # eval integer
            if math.modf(d)[1] > self.sec:
                self.sec = d
                return True
        
        def draw(self, render, st):
            if self.sleep(st):
                self.rx = random.randint(0, 1280)
                self.ry = random.randint(0, 720)

            width, height = render.get_size()
            if not isinstance(self.bg, renpy.Render):
                self.bg = renpy.render(self.bg, width, height, 0.0, 0.0)
            self.bgsize = self.bg.get_size()

            # true size of the box
            relw = (self.bgsize[0] - width) * self.rx // width
            relh = (self.bgsize[1] - height) * self.ry // height

            self.dx = relw - self.x
            self.dy = relh - self.y

            # travel speed
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))
        
        @property
        def meta(self):
            return (self.x, self.y, self.dx, self.dy, self.rx, self.ry)