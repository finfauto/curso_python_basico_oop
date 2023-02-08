class Partido:
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str):
        self.__fecha = fecha  # en UTC
        self.__lugar = lugar
        self._contendiente1 = contendiente1
        self._contendiente2 = contendiente2
        self._resultado = None

    def obtener_fecha(self, tz):
        # deberíamos tener en cuenta la tz pedida para devolver la fecha
        return self.__fecha

    def obtener_lugar(self):
        return self.__lugar

    def obtener_contendiente(self, local: bool):
        if local:
            return self._contendiente1
        return self._contendiente2

    def dar_resultado(self, resultado: str):
        self._resultado = resultado

    def imprimir_resumen(self):
        print(f"El partido disputado el {self.__fecha} en {self.__lugar} finalizó con reultado {self._resultado} y supuso que:")
        print(f"El contendiente {self._contendiente1} obtuviera {self.puntos_contendiente(self._contendiente1)} puntos")
        print(f"El contendiente {self._contendiente2} obtuviera {self.puntos_contendiente(self._contendiente2)} puntos")

    def puntos_contendiente(self, nombre_contendiente: str):
        raise NotImplementedError

    def _procesar_resultado(self):
        """
        Esta función devuelve dos enteros que corresponden a la puntuación obtenida en el partido por el contendiente local y por el visitante
        Debe ser específica para deporte. En tenis, por ejemplo, devolverá los sets ganados por cada contendiente. En fútbol, los goles, etc.
        """
        raise NotImplementedError


class PartidoConEmpate(Partido):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_empate: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2)
        self.__puntos_victoria = puntos_victoria
        self.__puntos_empate = puntos_empate
        self.__puntos_derrota = puntos_derrota

    def puntos_contendiente(self, nombre_contendiente: str):
        contendiente_ganador = self.__obtener_ganador()
        if contendiente_ganador == nombre_contendiente:
            return self.__puntos_victoria
        elif contendiente_ganador is None:
            return self.__puntos_empate
        return self.__puntos_derrota

    def __obtener_ganador(self):
        """
        En caso de que el resultado sea None, quiere decir que el resultado es un empate
        """
        resultado_local, resultado_visitante = self._procesar_resultado()
        if resultado_local > resultado_visitante:
            return self._contendiente1
        elif resultado_local < resultado_visitante:
            return self._contendiente2
        return None

    def _procesar_resultado(self):
        raise NotImplementedError


class PartidoSinEmpate(Partido):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2)
        self.__puntos_victoria = puntos_victoria
        self.__puntos_derrota = puntos_derrota

    def puntos_contendiente(self, nombre_contendiente: str):
        contendiente_ganador = self.__obtener_ganador()
        if contendiente_ganador == nombre_contendiente:
            return self.__puntos_victoria
        return self.__puntos_derrota

    def __obtener_ganador(self):
        """
        Solamente puede haber dos resultados en esta función. O gana un equipo o gana el otro
        """
        resultado_local, resultado_visitante = self._procesar_resultado()
        if resultado_local > resultado_visitante:
            return self._contendiente1
        return self._contendiente2

    def _procesar_resultado(self):
        raise NotImplementedError


class PartidoConEmpateFutbol(PartidoConEmpate):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_empate: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2, puntos_victoria, puntos_empate, puntos_derrota)

    def _procesar_resultado(self):
        return self._resultado.split("-")

# TODO: Partido sin empate fútbol. Con un resultado tipo: 2 (4)-(2) 2 que significaría que un equpo ha ganado por penalties


class PartidoSinEmpateBaloncesto(PartidoSinEmpate):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2, puntos_victoria, puntos_derrota)

    def _procesar_resultado(self):
        return self._resultado.split("-")


class PartidoSinEmpateTenis(PartidoSinEmpate):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2, puntos_victoria, puntos_derrota)

    def __obtener_ganador_set(self, resultado_set):
        juegos_local, juegos_visitante = resultado_set.split("-")
        if juegos_local > juegos_visitante:
            return self._contendiente1
        return self._contendiente2

    def _procesar_resultado(self):
        sets_contendiente_1 = 0
        sets_contendiente_2 = 0
        for resultado_set in self._resultado.split():
            ganador_set = self.__obtener_ganador_set(resultado_set)
            if ganador_set == self._contendiente1:
                sets_contendiente_1 += 1
            else:
                sets_contendiente_2 += 2
        return sets_contendiente_1, sets_contendiente_2


if __name__ == "__main__":
    partidos: [Partido] = []
    futbol1 = PartidoConEmpateFutbol("2022-11-07 21:00:00", "Estadio de Vallecas", "Rayo Vallecano", "Real Madrid", puntos_victoria=3, puntos_empate=1, puntos_derrota=0)
    futbol1.dar_resultado("3-2")
    partidos.append(futbol1)
    baloncesto1 = PartidoSinEmpateBaloncesto("2023-02-01 20:00:00", "Palacio de los Deportes de Madrid", "Real Madrid", "Panathinaikos", puntos_victoria=1, puntos_derrota=0)
    baloncesto1.dar_resultado("83-68")
    partidos.append(baloncesto1)
    tenis1 = PartidoSinEmpateTenis("2019-07-01 15:00:00", "Roland Garros", "Rafael Nadal", "Roger Federer", puntos_victoria=1, puntos_derrota=0)
    tenis1.dar_resultado("6-3 5-7 6-1 6-4")
    partidos.append(tenis1)

    for partido in partidos:
        partido.imprimir_resumen()
