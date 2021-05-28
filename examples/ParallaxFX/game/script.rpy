
init python:
    config.developer = True
    preferences.fullscreen   = True
    preferences.gl_tearing   = False
    preferences.gl_framerate = 60


screen magic_camera:
    add Bosque('1.png')

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
    call screen magic_camera

    e "Añade una historia, imágenes y música, ¡y puedes presentarlo al mundo!"

    return