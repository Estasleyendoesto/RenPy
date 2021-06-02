init python:

    class MyGames(Motionfx):
        def __init__(self, **kwargs):
            super(MyGames).__init__(**kwargs)

        def supergame(self, **kwargs):
            game = Supergame()
            self.attach(game, **kwargs)


    class Supergame:
        def __init__(self):
            self.aaa = "Soy un gran juego!"