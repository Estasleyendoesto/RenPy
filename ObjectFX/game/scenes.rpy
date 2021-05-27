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
            self.camfx = CamFX( bg, 0.01 )

            objfx = ObjectFX( self.camfx )
            objfx.add( Resource('peperana.png', [600, 600, 60, 40]) )
            self.objfx = objfx

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)
            self.objfx.fx_on(render)

        def on_event(self, e, x, y, st):
            self.camfx.mouse(x, y)

            obj1 = self.objfx.res[0]
            if obj1.hover:
                obj1.info = 'Peperana'
            if obj1.click(e):
                print("-----------------------------------")
                return 'Peperana'

        def on_update(self):
            pass