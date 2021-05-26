# Ren'Py Utils

Utilidades interesantes

> Creado el 25-05-2021



---

![](./assets/camfx.png)

## Efecto cámara

Un efecto cámara para acabar con las aburridas pantallas estáticas en nuestras novelas visuales.

```python
default preferences.fullscreen = True

screen magic_camera:
    add CamFX('room.png', 1280, 720)

label start:
    call screen magic_camera with dissolve
```

> El width y height no están implementados como debe de ser (que pereza), pero corregirlo es fácil.

<p align="center">
<img  src="./assets/camfx.gif">
</p>


---

![](./assets/parallax.png)

## Efecto parallax

Haciendo uso del efecto cámara se puede conseguir el efecto parallax de forma super simplificada para los eyes x e y, además de una velocidad de desplazamiento personalizada.

```python
default preferences.fullscreen = True

screen magic_camera:
    add Bosque('1.png')

label start:
    call screen magic_camera with dissolve
```

> La implementación es distinta a CamFX, se debe al uso de un gestor de escenarios para distribuir mejor la lógica dentro del juego (recomiendo su estructura). Los ficheros nuevos son: `engine.rpy`, `scenes.rpy`, `camFX.rpy`, `parallaxFX.rpy`.


<p align="center">
<img  src="./assets/parallax.gif">
</p>
