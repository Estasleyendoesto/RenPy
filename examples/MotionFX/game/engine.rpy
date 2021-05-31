#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: EngineFX
# version: 1.45
# description: Scene engine for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    """
    Creator-Defined Displayable básico que renderiza una escena precargada
    """
    class Engine(renpy.Displayable):
        scene = None

        def __init__(self, **kwargs):
            super(Engine, self).__init__(**kwargs)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            
            Engine.scene.on_update(st)
            Engine.scene.on_draw(render, width, height, st, at)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            return Engine.scene.on_event(ev, x, y, st)

        def visit(self):
            return []


init python:
    """
    Objeto abstracto, hereda de Engine y autoasigna la escena a renderizar
    """
    class Scene(Engine):
        def __init__(self, **kwargs):
            super(Scene, self).__init__(**kwargs)
            Engine.scene = self

        def on_draw(self, render, width, height, st, at):
            pass

        def on_event(self, event, x, y, st):
            pass

        def on_update(self, st):
            pass