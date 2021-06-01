init 1 python:
    from renpy.display.render import render as _render
    import pygame

    class Test(Scene):
        def __init__(self, bg, **kwargs):
            super(Test, self).__init__(**kwargs)
            self.bg = renpy.load_image(Image(bg))
            self.motion = Motionfx()

        def on_draw(self, render, width, height, st, at):
            render.blit(self.bg, (0,0))
            self.motion.draw(render, st)

        def on_event(self, e, x, y, st):
            self.motion.event(e, x, y, st)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.motion.dissolve('pepe.png', time=3.0, id=1)

        def on_update(self, st):
            pass