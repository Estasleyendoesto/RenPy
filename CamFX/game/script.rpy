
init python:
    config.developer = True
    preferences.fullscreen   = True
    preferences.gl_tearing   = False
    preferences.gl_framerate = 60


    class CamFX(renpy.Displayable):
        """
        La imagen del background debe ser de una resolución mayor a 1080p (según el juego, 2100p recomendado)
        Debido a las limitantes del juego, se recomienda jugar a pantalla completa (60fps, 30fps en modo ventana)
        Los atributos X e Y pueden definir la posición de otros objetos si se incluyen dentro del marco
        La velocidad de desplazamiento en flotante
        """

        def __init__(self, bg, **kwargs):
            super(CamFX, self).__init__(**kwargs)

            # Background
            self.bg = renpy.load_image( Image(bg) )
            self.bgsize = self.bg.get_size()

            # Posición inicial en el centro
            self.x = self.bgsize[0] // 4
            self.y = self.bgsize[1] // 4

            self.oldx = 0
            self.oldy = 0

            self.mouseX = 0
            self.mouseY = 0

            # Velocidad de desplazamiento (personalizable)
            self.speed = 0.008

        
        def fx_on(self, render):
            width, height = render.get_size()
            # El ancho y alto relativo al fondo y la ventana según la posición del cursor
            relw = (self.bgsize[0] - width) * self.mouseX // width
            relh = (self.bgsize[1] - height) * self.mouseY // height

            # La diferencia entre el punto A y B
            dx = relw - self.x
            dy = relh - self.y

            # Velocidad relativa a la distancia (más lejos, más rápido; más cerca, más lento)
            self.x += dx * self.speed
            self.y += dy * self.speed

            # Out of window fix
            if self.mouseX > 0 and self.mouseY > 0:
                self.oldx, self.oldy = self.x, self.y
            else:
                self.x, self.y = self.oldx, self.oldy

            # subsurface = recorte de la imagen de fondo
            bg = self.bg.subsurface( (self.x, self.y, width, height) )
            render.blit(bg, (0, 0))


        def render(self, width, height, st, at):
            render = renpy.Render(width, height)

            # Draw background
            self.fx_on(render)

            # Redraw
            renpy.redraw(self, 0)
            return render


        def event(self, event, x, y, st):
            self.mouseX = x
            self.mouseY = y

            return None


        def visit(self):
            return []


screen magic_camera:
    add CamFX('room.png')

    textbutton 'Close':
        align (1.0, 1.0)
        offset (-10, -10)
        action Return()


define e = Character("Eileen")
label start:
    scene bg room
    show eileen happy
    e "Has creado un nuevo juego Ren'Py."

    $ quick_menu = False
    call screen magic_camera with dissolve

    e "Añade una historia, imágenes y música, ¡y puedes presentarlo al mundo!"
    return