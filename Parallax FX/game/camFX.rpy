init python:
    class CamFX:
        def __init__(self, bg, speed = 0.01):
            # Background
            self.bg = renpy.load_image( Image(bg) )
            self.bgsize = self.bg.get_size()

            self.x = self.bgsize[0] // 4
            self.y = self.bgsize[1] // 4

            self.oldx = 0
            self.oldy = 0

            self.dx = 0
            self.dy = 0

            self.mouseX = 0
            self.mouseY = 0

            self.speed = speed

        
        def fx_on(self, render, width, height):
            relw = (self.bgsize[0] - width) * self.mouseX // width
            relh = (self.bgsize[1] - height) * self.mouseY // height

            self.dx = relw - self.x
            self.dy = relh - self.y

            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            if self.mouseX > 0 and self.mouseY > 0:
                self.oldx, self.oldy = self.x, self.y
            else:
                self.x, self.y = self.oldx, self.oldy

            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))


        def mouse(self, x, y):
            self.mouseX = x
            self.mouseY = y
        

        def meta(self):
            return (self.x, self.y, self.dx, self.dy, self.mouseX, self.mouseY)