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
            self.nigga = AliveFX('res/nigga.res', 0.460)
            self.lisa  = AliveFX('res/lisa.res', 0.080)
            self.banana  = AliveFX('res/banana.res', 0.120)
            self.aqua  = AliveFX('res/aqua.res', 0.300)
            self.doggie = AliveFX('res/doggie.res', 4.0)
            self.petia = AliveFX('res/petia.res', 0.280)
            self.goku  = AliveFX('res/goku.res', 2.80)

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)
            x, y = self.camfx.meta()[:2]

            self.nigga.on(render, st, 860 - x, 470 - y)
            self.lisa.on(render, st, 1377 - x, 593 - y)
            self.banana.on(render, st, 201 - x, 663 - y)
            self.aqua.on(render, st, 1170 - x, 779 - y)
            self.doggie.on(render, st, 561 - x, 703 - y)
            self.petia.on(render, st, 0 - x, 200 - y)
            self.goku.on(render, st, 890 - x, 730 - y)

        def on_event(self, event, x, y, st):
            self.camfx.mouse(x, y)

        def on_update(self):
            pass


    class Test2(Scene):
        def __init__(self, bg, **kwargs):
            super(Test2, self).__init__(**kwargs)
            self.camfx = CamFX( bg, 0.05 )
            self.alivefx = AliveFX('res/landscape.res', 0.78)
            self.alivefx.landscape = True

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)

            x, y = self.camfx.meta()[:2]
            self.alivefx.on(render, st, x, y)

        def on_event(self, event, x, y, st):
            self.camfx.mouse(x, y)

        def on_update(self):
            pass