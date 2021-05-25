# Ren'Py Utils

Utilidades interesantes





![](./assets/camfx.png)

## Efecto cámara

Un efecto cámara para acabar con las aburridas pantallas estáticas en nuestras novelas visuales.

```python
default preferences.fullscreen = True

screen magic_camera:
    add CamFx('room.png', 1280, 720)

label start:
    call screen magic_camera with dissolve
```

> El width y height no están implementados como debe de ser (pereza), pero corregirlo es fácil.

