init python:
    config.developer = True
    preferences.fullscreen   = False
    preferences.gl_tearing   = False
    preferences.gl_framerate = 60
    config.save_dump = True

    renpy.add_layer('fx', above='master', menu_clear=True)

screen magic_camera:
    $ renpy.free_memory()
    layer 'fx'
    add Test('doraemon.jpg')
    frame:
        align (0, 0)
        background 'blur.png'

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