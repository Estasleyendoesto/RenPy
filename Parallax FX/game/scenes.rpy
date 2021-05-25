init 1 python:

    class Bosque(Scene):
        def __init__(self, bg, **kwargs):
            super(Bosque, self).__init__(**kwargs)
            self.camfx = CamFX( bg, 0.05 )

            parallax = ParallaxFX( self.camfx )

            # Jugar con el delay para conseguir la velocidad deseada
            # delay = 0, misma velocidad que la cámara
            parallax.add('2.png', 0.00)
            parallax.add('3.png', 0.01)
            parallax.add('4.png', 0.02)
            parallax.add('5.png', 0.03)
            parallax.add('6.png', 0.04)
            parallax.add('7.png', 0.05)
            parallax.add('8.png')

            self.parallax = parallax


        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render, width, height)
            self.parallax.on(render)

        def on_event(self, event, x, y, st):
            self.camfx.mouse(x, y)

        def on_update(self):
            pass