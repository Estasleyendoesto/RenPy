#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name: FX
# version: 1.0
# description: Effects for Ren'Py Engine
# author: Estasleyendoesto
# site: https://github.com/Estasleyendoesto/RenPy

init -1 python:
    import cPickle
    import pygame
    import base64
    import math
    import os
    import io

    # Layer
    preferences.gl_framerate = 60
    renpy.add_layer('fx', above='master', menu_clear=False)
    # etc...
    class Engine(renpy.Displayable):
        """
        Basic Creator-Defined Displayable rendering a preloaded scene
        """

        scene = None

        def __init__(self, **kwargs):
            super(Engine, self).__init__(**kwargs)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            
            Engine.scene.on_update(st)
            Engine.scene.on_draw(render, width, height, st)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            return Engine.scene.on_event(ev, x, y, st)

        def visit(self):
            return []

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

    class Camfx:
        """
        Camera effect simulator based on Creator-Defined Displayables
        The constructor receives the following:
            - bg = '*.png|jpeg|webp' or '1280x720' (required)
            - speed = 0.000 (scroll speed)

        The meta method returns what is required for its own integrations.
        *Dissolve effect for transition not recommended
        """

        def __init__(self, bg, speed = 0.001):
            if os.path.splitext(bg)[1]:
                res = renpy.displayable(bg)
            else:
                i = list(bg).index('x')
                w, h = int(bg[:i]), int(bg[i+1:])
                solid = Solid((0,0,0, 0), xsize=w, ysize=h)
                res = renpy.displayable(solid)

            self.bg = res
            self.bgsize = None
            self.x = 0
            self.y = 0

            self.oldx = 0
            self.oldy = 0

            self.dx = 0
            self.dy = 0

            self.mouseX = 0
            self.mouseY = 0

            self.speed = speed
        
        def draw(self, render):
            # true size of the box
            width, height = render.get_size()
            if not isinstance(self.bg, renpy.Render):
                self.bg = renpy.render(self.bg, width, height, 0.0, 0.0)

            self.bgsize = self.bg.get_size()

            relw = (self.bgsize[0] - width) * self.mouseX // width
            relh = (self.bgsize[1] - height) * self.mouseY // height

            self.dx = relw - self.x
            self.dy = relh - self.y

            # travel speed
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            # out of box fix
            if self.mouseX > 0 and self.mouseY > 0:
                self.oldx, self.oldy = self.x, self.y
            else:
                self.x, self.y = self.oldx, self.oldy

            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))

        def mouse(self, x, y):
            self.mouseX = x
            self.mouseY = y
        
        @property
        def meta(self):
            return (self.x, self.y, self.dx, self.dy, self.mouseX, self.mouseY)

    class Layer:
        """
        It is important for Parallaxfx to function properly.
        """

        def __init__(self, bg, delay=0.00):
            self.delay = delay
            self.bg    = bg
            # aux
            self.x = 0
            self.y = 0
            self.oldx = 0
            self.oldy = 0

        def axis(self):
            return self.x, self.y

    class Parallaxfx:
        """
        If last layer is "unstable" or "vibrates", delay 0.0 to correct it.
        Important to define the displacement speed for each layer.
        You can select to apply the effect on x-axis, y-axis or both together.
        Different speed could be defined for x and y (in development)

        Constructor receives as parameters:
            - Camfx object (required)

        Add method receives as parameters:
            - bg = '*.png|jpeg|webp'
            - delay = 0.00 (0 = same speed as camera)
        """

        def __init__(self, camfx):
            self.camfx = camfx
            self.layers = []
            # Enable x, y axis
            self.x_on = True
            self.y_on = False

        def optimize(self, bg):
            if isinstance(bg, str):
                return renpy.load_image( Image(bg) )
            return bg

        def draw(self, render):
            width, height = render.get_size()
            x, y, dx, dy, mouseX, mouseY = self.camfx.meta

            for layer in self.layers:
                # custom speed
                if self.x_on:
                    x += dx * layer.delay
                if self.y_on:
                    y += dy * layer.delay

                # out of box fix
                if mouseX > 0 and mouseY > 0:
                    layer.oldx, layer.oldy = x, y
                else:
                    x, y = layer.oldx, layer.oldy

                # aux
                layer.x = x
                layer.y = y
 
                # progresive loader
                layer.bg = self.optimize(layer.bg)
                # cut and draw
                bg = layer.bg.subsurface( (x, y, width, height) )
                render.blit(bg, (0, 0))

        def add(self, *arg, **kwargs):
            self.layers.append( Layer(*arg, **kwargs) )

        def delete(self, index):
            self.layers.pop(index)

    class Resource:
        """
        It is important for the operation of Objectfx
        """

        _ev = None

        def __init__(self, image, x=0, y=0, mask=False, layer=None):
            self.image = renpy.displayable(image)
            self.hover = False
            self.layer = layer      # required if parallax is active
            self.mask  = mask
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

        def __init__(self, cam=None, parallax=None):
            self.parallax = parallax
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
                    if self.parallax:
                        try:
                            axis = self.parallax.layers[res.layer].axis()
                            x, y = [a-b for a,b in zip(res.rect[:2], axis)]
                        except:
                            pass
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
                    if res.mask:
                        binx, biny = int(mx-x), int(my-y)
                        if binx > 0 and biny > 0:
                            res.hover = ren.is_pixel_opaque(binx, biny)
                    else:
                        res.hover = True
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

        def add(self, *arg, **kwargs):
            self.res.append( Resource(*arg, **kwargs) )

        def delete(self, index):
            self.res.pop(index)

    class Animate:
        """
        It is important for Alivefx to function properly.
        """

        def __init__(self, res, delay=0.0, loop=0, rever=False, landscape=False, x=0, y=0, layer=None):
            # file = config.basedir + "/game\\" + res
            file = os.path.join(config.gamedir, 'images/' + res)
            res  = cPickle.load( open(file, 'rb') )
            self.frames = [ io.BytesIO(base64.b64decode( frame )) for frame in res ]

            self.loop  = loop  # 0 = inf
            self.delay = delay # millis (per frame, 0.001 -> 1.0)
            self.rever = rever # zigzag animation

            self.x, self.y = x, y

            self.layer = layer
            
            # experimental
            self.landscape = landscape

            # aux
            self.pos   = 0
            self.sec   = 0.0
            self.times = 0
            self.delta = 0

        def tracker(self):
            if self.rever:
                # start = +1, end = -1
                if self.pos == 0 : self.delta = 1
                if self.pos == len(self.frames) - 1 : self.delta = -1
                self.pos += self.delta
            else:
                self.pos += 1 if self.pos < len(self.frames) - 1 else -self.pos

        def looper(self):
            if self.loop:
                # num of repeats
                if self.times < self.loop + 1:  # Little cheat
                    if not self.pos:
                        self.times += 1
                else:
                    return False
                    
            return True

        def sleeper(self, st):
            duration = self.delay
            duration = 0.001 if not duration else duration
            # custom acceleration equation
            t = duration * 1000
            v = len(self.frames) / t
            d = st / v
            # eval integer
            if math.modf(d)[1] > self.sec:
                self.sec = d
                return True

        def optimize(self):
            frame = self.frames[self.pos]
            # progresive loader
            if isinstance(frame, io.BytesIO):
                frame = pygame.image.load(frame)
                self.frames[self.pos] = frame

            return frame

        def sleeperOLD(self):
            self.sec += 0.1
            if self.sec > self.delay:
                self.sec -= self.sec
                return True

    class Alivefx:
        """
        Alivefx is a tool for displaying image sequences.
        It can be used on its own displayable or together with Camfx with its functionalities.
        By activating landscape it can be used in animated background mode.
        The constructor can receive the following:
            - res = '*.res' (required)
            - delay = 0.000
            - loop = 0
            - rever = False
            - landscape = False
        """

        def __init__(self):
            self.parallax = None
            self.camfx    = None
            self.animes   = []

        def draw(self, render, st):
            for anime in self.animes:
                # Rules
                if anime.sleeper(st):
                    if anime.looper():
                        anime.tracker()
                
                frame = anime.optimize()
                # original axis
                x = anime.x
                y = anime.y
                # Experimental
                if anime.landscape:
                    width, height = render.get_size()
                    frame = frame.subsurface( (x, y, width, height) )
                    x, y = 0, 0
                else:
                    if self.camfx:
                        x, y = self.camfx.meta[:2]
                    if self.parallax:
                        try:
                            x, y = self.parallax.layers[anime.layer].axis()
                        except:
                            pass
                    x = anime.x - x
                    y = anime.y - y
                # Esto no xD
                render.blit( frame, (x, y) )

        def add(self, *args, **kwargs):
            self.animes.append( Animate(*args, **kwargs) )

        def delete(self, index):
            self.animes.pop(index)
    
    class FX:
        """
        Class constructor of all libraries fx
        Each method automatically adds the functionalities of each fx library
        """

        def __init__(self):
            self.camfx    = None
            self.parallax = None
            self.objectfx = None
            self.alivefx  = None

        def draw(self, render, st):
            if self.camfx:
                self.camfx.draw(render)
            if self.parallax:
                self.parallax.draw(render)
            if self.alivefx:
                self.alivefx.draw(render, st)
            if self.objectfx:
                self.objectfx.draw(render)

        def action(self, ev, x, y, st):
            if self.camfx:
                self.camfx.mouse(x, y)
            if self.objectfx:
                self.objectfx.event(ev, x, y)

        def camera(self, *args, **kwargs):
            self.camfx = Camfx(*args, **kwargs)

        def layer(self, *args, **kwargs):
            if self.camfx is None:
                raise Exception("camfx object doesn't exists")
            if self.parallax is None:
                self.parallax = Parallaxfx(self.camfx)
                
            self.parallax.add(*args, **kwargs)

        def object(self, *args, **kwargs):
            if self.objectfx is None:
                self.objectfx = Objectfx()
                if self.camfx:
                    self.objectfx.cam = self.camfx
                if self.parallax:
                    self.objectfx.parallax = self.parallax

            self.objectfx.add(*args, **kwargs)

        def alive(self, *args, **kwargs):
            if self.alivefx is None:
                self.alivefx = Alivefx()
                if self.camfx:
                    self.alivefx.cam = self.camfx
                if self.parallax:
                    self.alivefx.parallax = self.parallax

            self.alivefx.add(*args, **kwargs)

        def delete(self, fx, index):
            if fx == 'layer':
                
                self.parallax.delete(index)
            if fx == 'object':
                self.objectfx.delete(index)
            if fx == 'alive':
                self.alivefx.delete(index)