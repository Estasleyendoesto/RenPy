
init 1 python:
    renpy.add_layer('fx', above='master', menu_clear=False) # no sirve pero me gusta

    def save(): # hay que probar si funciona realmente el save
        config.skipping = None
        renpy.checkpoint()
        renpy.block_rollback()
        renpy.retain_after_load()

    def mostrar():  # borrar (tempral)
        print('tiempo')

    class Test(Scene):
        def __init__(self, bg, **kwargs):
            super(Test, self).__init__(**kwargs)

            fx = FX()
            fx.camera('px/1.png', 0.05)
            # Parallax
            fx.layer('px/2.png', 0.00)
            fx.layer('px/3.png', 0.01)
            fx.layer('px/4.png', 0.02)
            fx.layer('px/5.png', 0.03)
            fx.layer('px/6.png', 0.04)
            fx.layer('px/7.png', 0.05)
            fx.layer('px/8.png')
            # Frames sequence
            fx.alive('lisa.res', 0.080, x=1250, y=710, layer=6)
            # Objects
            fx.object('dog1.png', 580, 610, mask=True, layer=6)

            self.fx = fx

        def on_draw(self, render, width, height, st):
            self.fx.draw(render, st)


        def on_event(self, event, x, y, st):
            self.fx.action(event, x, y, st)
            # Object event
            dog = self.fx.objectfx.res[0]
            if dog.hover:
                dog.info = Text('dogecoin', color='#fff') 
            if dog.click:
                self.fx.delete('layer', 6)

        def on_update(self, st):
            pass