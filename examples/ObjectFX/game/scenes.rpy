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
            objfx.add('dog1.png', [580, 550, 332, 385], 'dog1.dat')

            self.objfx = objfx

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)
            self.objfx.fx_on(render)

        def on_event(self, e, x, y, st):
            self.camfx.mouse(x, y)

            obj1 = self.objfx.res[0]
            if obj1.hover:
                obj1.info = Text('Dogecoin', color="#fff")
            if obj1.click(e):
                pass

        def on_update(self, st):
            pass