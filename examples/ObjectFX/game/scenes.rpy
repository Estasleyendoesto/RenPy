init 1 python:
    class Test(Scene):
        def __init__(self, bg, **kwargs):
            super(Test, self).__init__(**kwargs)
            self.camfx = CamFX( bg, 0.05 )

            self.objects = Objectfx( self.camfx )
            self.objects.add('dog1.png', 580, 550)
            self.objects.add('dog2.png', 1003, 700)
            self.objects.add('pepe.png', 1796, 880)

        def on_draw(self, render, width, height, st):
            self.camfx.draw(render)
            self.objects.draw(render)

        def on_event(self, e, x, y, st):
            self.camfx.mouse(x, y)
            self.objects.event(e, x, y)

            dog = self.objects.res[0]
            if dog.hover:
                dog.info = Text('Dogecoin', color="#fff")
            if dog.click:
                dog.info = 'talk.png'

            frog = self.objects.res[2]
            if frog.hover:
                frog.info = Text('Peperana', color="#c9c9c9")

            return None

        def on_update(self, st):
            pass