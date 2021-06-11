#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: CamFX
# version: 1.0
# description: Camera effect for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    config.developer = True
    preferences.fullscreen   = False
    preferences.gl_tearing   = False
    preferences.gl_framerate = 60

    class MyD(renpy.Displayable):
        
        def __init__(self, bg, **kwargs):
            super(MyD, self).__init__(**kwargs)
            self.eyemove = AutocamFX( bg, 0.02 )

            self.sec = 0.0
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
           
            # Autocam Effect
            self.eyemove.draw(render, st)

            # Redraw
            renpy.redraw(self, 0)
            return render

        def event(self, event, x, y, st):
            return None

        def visit(self):
            return []


screen magic_camera:
    default d = MyD('anime.png')
    add d
    # Se puede usar un tamaño distinto para el Displayable
    # add MyD('room.png'):
    #    size (800, 600)
    #    align (0.5, 0.5)

    textbutton 'Close':
        align (1.0, 1.0)
        offset (-10, -10)
        action Return()


define e = Character("Eileen")
label start:
    scene bg room
    show eileen happy
    e "Has creado un nuevo juego Ren'Py."

    $ quick_menu = False
    call screen magic_camera

    e "Añade una historia, imágenes y música, ¡y puedes presentarlo al mundo!"
    return