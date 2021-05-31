#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: objectFX
# version: 3.1
# description: Objects insertion for camFX engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init python:
    import pygame

    class Resource:
        """
        It is important for the operation of Objectfx
        """

        _ev = None

        def __init__(self, image, x=0, y=0):
            self.image = renpy.displayable(image)
            self.hover = False
            self.rect  = [x, y]     # required
            self.info  = None       # Text() or image route (None = off)

        @property
        def click(self):
            try:
                ev = Resource._ev
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    return True if self.hover else False
            except:
                pass


    class Objectfx:
        """
        It can be used in its own displayable or integrated with Camfx.
        Resources are created automatically with the add() method.

        The add() method receives the following parameters:
            - image = str (required)
            - x and y = the position of the object on the base background
            
        To capture an event associated with an object:
            - objectfx.res[index].hover (if)
            - objectfx.res[index].click (if)
        """

        def __init__(self, cam=None):
            self.cam = cam
            self.res = []
            self.aux = []

        def draw(self, render):
            w, h = render.get_size()
            for res in self.res:
                ren = renpy.render(res.image, w, h, 0.0, 0.0)
                # getting resource size
                if len(res.rect) < 4:
                    res.rect.extend(ren.get_size())
                # current x and y
                if self.cam:
                    x, y = [a-b for a,b in zip(res.rect[:2], self.cam.meta[:2])]    
                else:
                    x, y = res.rect[:2]
                # draw resource
                render.blit(ren, (x, y))
                # collision event
                self._event(res, ren, x, y)

            # floating text
            for res in self.res:
                self.info(render, res)

        def event(self, ev, x, y):
            Resource._ev = ev
            self.aux = [x, y]

        def _event(self, res, ren, x, y):
            try:
                mx, my = self.aux
                w, h = res.rect[-2:]
                # Rect Collision
                if x <= mx < x+w and y <= my < y+h:
                    # Mask collission
                    binx, biny = int(mx-x), int(my-y)
                    if binx > 0 and biny > 0:
                        res.hover = ren.is_pixel_opaque(binx, biny)
                else:
                    res.hover = False
            except:
                pass

        def info(self, render, res):
            if res.info and res.hover:
                # render from displayable
                d = renpy.displayable(res.info) 
                width, height = render.get_size()
                info = renpy.render(d, width, height, 0, 0)
                
                size = info.get_size()
                x, y = self.aux[-2:]
                # custom location (you can edit this)
                x -= size[0]
                y -= size[1]
                # draw render
                render.blit(info, (x, y))

        def add(self, *resource):
            self.res.append( Resource(*resource) )