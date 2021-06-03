init python:
    config.developer = True
    preferences.fullscreen   = False
    preferences.gl_tearing   = False
    preferences.gl_framerate = 60


screen magic_camera():
    $ save()                # no se si vladra
    layer 'fx'          # no sirve pero me gusta (creo que no sirve, probar sin él si guarda)
    # add test
    default test = Test('fondo.jpg')    # con default se guarda el objeto en el save, y podemos aprovechar el return
    add test    #invocamos
    $ ui.timer(delay=1.0, repeat=True, action=[Function(mostrar)])  # temporizador para el reloj

    textbutton 'Close':
        align (1.0, 1.0)
        offset (-10, -10)
        action Return()

define e = Character("Eileen")
label start:
    scene bg room
    show eileen happy
    e "Has creado un nuevo juego Ren'Py."

    # default engine = Engine()
    # default test = Test('fondo.jpg')
    # default scache = Scenecache()

    $ quick_menu = False
    call screen magic_camera()

    e "Añade una historia, imágenes y música, ¡y puedes presentarlo al mundo!"

    return