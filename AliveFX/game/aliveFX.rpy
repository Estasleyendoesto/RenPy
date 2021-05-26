#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: AliveFX
# version: 1.0
# description: Image sequence for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    # from PIL import Image
    
    class AliveFX:
        def __init__(self, res):
            file = renpy.file(res).name
            print(file)


            self.resource = res