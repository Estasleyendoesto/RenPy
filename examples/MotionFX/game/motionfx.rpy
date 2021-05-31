init python:
    # Documentación: https://www.renpy.org/doc/html/atl.html#list-of-transform-properties
    # Examinar renpy/display/transform.py para el uso de sus funcionalidades
    # Examinar renpy/display/transition.py ahorrar ciertas fórmulas


    # La forma ideal de cómo usarlo está en scenes
    # El problema es que tras llamar un motion, al finalizar su reproducción desaparece
    # Se necesita que se almacene el motion eternamente (si no se especifica lo contrario) 
    # Pero si se exigiera que se repitiera el motion de principio a fin (buscar solución)
    # También que almacene el resultado final del motion si no se quiere que se repita

    # El problema con dissolve() está que tras la reproducción ocurre uno de los problemas anteriores
    # La variable aux soluciona el problema de duración del evento
    # Se requiere implementar un controlador "event" que bloquee la reproducción tras activarlo
    # Y que no se vuelva a activar más o que tal vez se vuelva a reproducir tras activar

    class Motion:
        """
        """

        def __init__(self, id, items, props):
            self.id = id
            self.items = items
            self.props = props


    class Motionfx:
        """
        """

        def __init__(self):
            self.motion = []
            self.record = []

        def draw(self, render, st):
            index = 0
            for motion in self.motion:
                method = getattr(self, motion.props['method'])
                method( index, render, st, **motion.props )
                index += 1

        def event(self, ev, x, y, st):
            self.record = [ev, x, y, st]

        def attach(self, dict, id, items=1):
            object = None
            if id:
                for motion in self.motion:
                    if motion.id == id:
                        object = motion
                        break
            if object is None:
                self.motion.append(Motion(id, items, dict))   
            else:
                if 0<object.items>1:
                    object.items -= 1
                    self.motion.append(Motion(object.id, 1, dict))

        def dissolve(self, image, time, unique=None, id=None, items=None):
            dict = {
                'image': image,
                'time' : time,
                'start': self.record[3],
                'unique': unique,
                'method': '_dissolve'
            }
            
            self.attach(dict, id, items)

        def _dissolve(self, index, render, st, **props):
            width, height = render.get_size()
            image = props['image']
            init  = props['start']
            time  = props['time']

            st -= init
            if st < time:
                limit  = (st + time) / time   # dejamos st solo para al revés
                start  = -1.0                 # 1.0 al revés
                end    = 8 / 256.0
                offset = start + (end - start) * limit

                d = Transform(child=image, alpha=offset)     
            else:
                if not props['unique']:
                    self.motion.pop(index)
                else:
                    d = renpy.displayable(image)

            re = renpy.render(d, width, height, st, 0)
            render.blit(re, (0,0))

                

            """
                self.motion[index].props['offset'] = offset
            

            offset = self.motion[index].props['offset']
            render.place( Text( str(offset) ), x=10, y=10 )

            if st < init + time:
                # render.place( Text( str('ahoy!!') ), x=10, y=10 )
                
            else:
            """  


    # render.place( Text( str(st) ), x=10, y=10 )



    class MotionFXa:
        def __init__(self):
            self.motion = None
            self.event = False
            self.aux = None

            self.store = []

        def on(self, render, st):
            self.render = render
            self.st = st

            if self.motion:
                method = getattr(self, self.motion[0])
                args = self.motion[1:] + [render, st]
                method(*args)

            if self.store:
                pass

        def dissolve(self, image, time):
            self.event  = True
            self.motion = ['_dissolve', image, time]
            
        def _dissolve(self, image, time, render, st):
            width, height = render.get_size()

            # Falta arreglar con aux (pero la idea funciona)
            # aux contiene el tiempo que debe alcanzar st para terminar la animación
            # el problema es que al terminar el tiempo desaparece la imagen
            # si se corrigen los problemas anteriores se corrige este y de los futuros motions
            # también está el optimizar la carga de la imagen (si renpy no lo hace, verificar)
            if not self.aux:
                self.aux = st + time

            if st > self.aux:
                pass


            if st > time + self.aux:
                self.motion = None
                self.aux = None

            limit  = st / time
            start  = -1.0
            end    = 8 / 256.0
            offset = start + (end - start) * limit

            t  = Transform(child=image, alpha=offset)
            re = renpy.render(t, width, height, st, 0)
            render.blit(re, (0,0))