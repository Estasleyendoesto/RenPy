init 1 python:
    class Layer:
        """
        Es importante para el funcionamiento de ParallaxFX
        Almacena un surface de la imagen, su delay y memoriza su posición en x e y
        """

        def __init__(self, bg, delay = 0):
            self.delay = delay
            self.bg = renpy.load_image( Image(bg) )

            self.oldx = 0
            self.oldy = 0


    class ParallaxFX:
        """
        Es importante el uso de CamFX para hacerlo funcionar (hace uso de sus cálculos)
        Si se establece la velocidad a 0.0 se moverá a la misma velocidad que la cámara
        Puede seleccionar aplicar el efecto en el eje x, y, o ambos juntos
        Es importante definir la velocidad de desplazamiento para cada layer
        Con pequeños cambios, también podría definirse una velocidad distinta para x e y
        Si la última capa es "inestable" o "vibra", delay a 0.0 para corregirlo
        """

        def __init__(self, camfx):
            self.camfx = camfx
            self.layers = []
            self.x_on = True
            self.y_on = False


        def on(self, render):
            width, height = render.get_size()
            x, y, dx, dy, mouseX, mouseY = self.camfx.meta()

            for layer in self.layers:
                if self.x_on:
                    x += dx * layer.delay
                if self.y_on:
                    y += dy * layer.delay

                if mouseX > 0 and mouseY > 0:
                    layer.oldx, layer.oldy = x, y
                else:
                    x, y = layer.oldx, layer.oldy

                bg = layer.bg.subsurface( (x, y, width, height) )
                render.blit(bg, (0, 0))


        def add(self, bg, delay = 0):
            self.layers.append( Layer(bg, delay) )