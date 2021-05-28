#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: objectFX
# version: 2.7
# description: Objects insertion for camFX engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    import cPickle
    import pygame

    import time

    class Resource:
        def __init__(self, image='', rect=[], mask=False):
            self.image = image
            self.hover = False
            self.info  = None # Text() or image route (None = off)
            self.mask  = mask
            self.rect  = rect

            if mask:
                # Ligero retraso al abrir (puede reducirse a 0 sacrificando la predicción de renpy)
                file = renpy.file(mask).name 
                start = time.time()
                self.mask = cPickle.load( open(file, 'rb') )
                end = time.time()
                print(end - start)

        def click(self, event):
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True


    class ObjectFX:
        def __init__(self, cam):
            self.cam = cam
            self.res = []

        def fx_on(self, render):
            for res in self.res:
                self.draw(render, res)
            for res in self.res:
                self.info(render, res)

        def draw(self, render, res):
            # Interpretation of X and Y
            x, y = [a - b for a, b in zip(res.rect[:2], self.cam.meta()[:2])]
            if res.image:
                re = renpy.load_image(Image(res.image))
                render.blit(re, (x, y))

            self.event(res, x, y)

        def event(self, res, x, y):
            mouseX, mouseY = self.cam.meta()[-2:]
            width, height  = res.rect[-2:]

            # Rect Collision
            if (mouseX > x and mouseX < x + width) and (mouseY > y and mouseY < y + height):
                # Mask Collision
                if res.mask:
                    binx, biny = int(mouseX - x), int(mouseY - y)
                    if binx > 0 and biny > 0:
                        res.hover = True and res.mask[biny][binx] or False
                else:
                    res.hover = True
            else:
                res.hover = False

        def info(self, render, res):
            if res.info and res.hover:
                d = renpy.displayable(res.info) 
                # render from displayable
                width, height = render.get_size()
                info = renpy.render(d, width, height, 0, 0)
                
                size = info.get_size()
                x, y = self.cam.meta()[-2:]
                # custom location (you can edit this)
                x -= size[0]
                y -= size[1]

                render.blit(info, (x, y))

        def add(self, *res):
            self.res.append( Resource(*res) )