#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: EngineFX
# version: 1.7
# description: Scene engine for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    class Engine(renpy.Displayable):
        """
        Basic Creator-Defined Displayable rendering a preloaded scene
        """

        scene = None

        def __init__(self, **kwargs):
            super(Engine, self).__init__(**kwargs)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            
            self.scene.on_update(st)
            self.scene.on_draw(render, width, height, st)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            return self.scene.on_event(ev, x, y, st)

        def visit(self):
            return []


init python:
    class Scene(Engine):
        """
        Abstract object, inherits from Engine and self-assigns the scene to be rendered
        """

        def __init__(self, **kwargs):
            super(Scene, self).__init__(**kwargs)
            Engine.scene = self

        def on_draw(self, render, width, height, st):
            pass

        def on_event(self, event, x, y, st):
            pass

        def on_update(self, st):
            pass