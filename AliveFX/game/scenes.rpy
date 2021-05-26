#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: ParallaxFX
# version: 1.0
# description: Parallax Effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init 1 python:

    class Test(Scene):
        def __init__(self, bg, **kwargs):
            super(Test, self).__init__(**kwargs)
            self.bg = renpy.load_image( Image(bg) )

            self.alivefx = AliveFX('nigga.res')


        def on_draw(self, render, width, height, st):
            render.blit(self.bg, (0, 0))
            self.alivefx.on(render)

        def on_event(self, event, x, y, st):
            pass

        def on_update(self):
            pass