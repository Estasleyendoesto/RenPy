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
            self.camfx = CamFX( bg, 0.05 )
            self.alivefx = AliveFX('nigga.res', 0.3)

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)

            x, y = self.camfx.meta()[:2]
            self.alivefx.on(render, 860 - x, 470 - y)

        def on_event(self, event, x, y, st):
            self.camfx.mouse(x, y)

        def on_update(self):
            pass


    class Test2(Scene):
        def __init__(self, bg, **kwargs):
            super(Test2, self).__init__(**kwargs)
            self.camfx = CamFX( bg, 0.05 )
            self.alivefx = AliveFX('landscape.res', 0.3)
            self.alivefx.landscape = True

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)

            x, y = self.camfx.meta()[:2]
            self.alivefx.on(render, x, y)

        def on_event(self, event, x, y, st):
            self.camfx.mouse(x, y)

        def on_update(self):
            pass