init python:
    import cPickle
    import pygame

    class Resource:
        def __init__(self, img='', rect=[], mask=None):
            self.image = img if img else ''
            self.hover = False
            self.rect = rect

            self.info = ''

            # Ligero retraso al abrir (puede reducirse a 0 sacrificando la predicción de renpy)
            if mask:
                file = renpy.file(mask).name 
                self.mask  = cPickle.load( open(file, 'rb') )
            else:
                self.mask = False

        def click(self, event):
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
                
                return False

            

    class ObjectFX:
        def __init__(self, cam):
            self.cam = cam
            self.res = []

        
        def fx_on(self, render):
            # Para cada recurso
            for res in self.res:
                self.draw(render, res)
                self.textinfo(render, res)
            
        
        def draw(self, render, res):
            # Verdadero valor de x e y
            x, y = [a - b for a, b in zip(res.rect[:2], self.cam.meta()[:2])]
            # Si imagen existe, mostrar
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

        def add(self, res):
            self.res.append(res)


        def textinfo(self, render, res):
            if res.info and res.hover:
                text = res.info
                x, y = self.cam.meta()[:2]
                mouseX, mouseY = self.cam.meta()[-2:]

                # X correction
                latin = 0
                for c in (' ', 'i', 'I', 'l', 't', 'j'):
                    latin += text.count(c)

                fix = (len(text) - latin) * 12 + (latin * 14)

                if x < 250:
                    x = mouseX + 30
                else:
                    x = mouseX - fix + (-10 if len(text) > 10 else 0)

                # Y Correction
                if y < 40:
                    y = mouseY + 10
                else:
                    y = mouseY - 23

                # Draw
                render.place( Text(text, color="#fff"), x=x, y=y )