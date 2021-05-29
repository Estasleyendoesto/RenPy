init 1 python:

    class Test(Scene):
        def __init__(self, bg, **kwargs):
            super(Test, self).__init__(**kwargs)
            self.camfx = CamFX( bg, 0.05 )

            objfx = ObjectFX( self.camfx )
            objfx.add('dog1.png', [580, 550, 332, 385],  'dog1.dat')
            objfx.add('dog2.png', [1003, 700, 164, 223], 'dog2.dat')
            objfx.add('pepe.png', [1796, 880, 60, 40],  'pepe.dat')
            self.objfx = objfx

        def on_draw(self, render, width, height, st):
            self.camfx.fx_on(render)
            self.objfx.fx_on(render)

        def on_event(self, e, x, y, st):
            self.camfx.mouse(x, y)

            dog = self.objfx.res[0]
            if dog.hover:
                dog.info = Text('Dogecoin', color="#fff")
            if dog.click(e):
                dog.info = 'talk.png'

        def on_update(self, st):
            pass