#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: EngineFX
# version: 1.0
# description: Scene engine for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
     class Engine(renpy.Displayable):
        scene = None

        def __init__(self, **kwargs):
            super(Engine, self).__init__(**kwargs)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            
            self.scene.on_update()
            self.scene.on_draw(render, width, height, st)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            self.scene.on_event(ev, x, y, st)

        def visit(self):
            return []


init python:
    class Scene(Engine):
        def __init__(self, **kwargs):
            super(Scene, self).__init__(**kwargs)
            Engine.scene = self

        def on_draw(self, render, width, height, st):
            pass

        def on_event(self, event, x, y, st):
            pass

        def on_update(self):
            pass