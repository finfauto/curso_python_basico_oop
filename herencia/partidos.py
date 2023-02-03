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

    # TODO: función que devuelve si un contendiente dado por parámetro participa en el partido

    def puntos_contendiente(self, nombre_contendiente: str):
        raise NotImplementedError

    def dar_resultado(self, resultado: str):
        raise NotImplementedError

    def imprimir_resumen(self):
        # TODO: Implementar aquí
        raise NotImplementedError


class PartidoFutbol(Partido):
    def __init__(self, fecha: str, lugar: str, contendiente1: str, contendiente2: str, puntos_victoria: int, puntos_empate: int, puntos_derrota: int):
        super().__init__(fecha, lugar, contendiente1, contendiente2)
        self.__puntos_victoria = puntos_victoria
        self.__puntos_empate = puntos_empate
        self.__puntos_derrota = puntos_derrota

    def puntos_contendiente(self, nombre_contendiente: str):
        contendiente_ganador = self.__obtener_ganador()
        if contendiente_ganador is None:  # empate
            return self.__puntos_empate
        elif contendiente_ganador == nombre_contendiente:
            return self.__puntos_victoria
        return self.__puntos_derrota

    def __obtener_ganador(self):
        goles_local, goles_visitante = self._resultado.split("-")
        if goles_local > goles_visitante:
            return self._contendiente1
        elif goles_local < goles_visitante:
            return self._contendiente2
        return None

    def dar_resultado(self, resultado: str):
        # TODO: Comprobar que el resultado es válido para un partido de fútbol
        self._resultado = resultado


class PartidoBaloncesto(Partido):
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
        puntos_local, puntos_visitante = self._resultado.split("-")
        if puntos_local > puntos_visitante:
            return self._contendiente1
        return self._contendiente2

    def dar_resultado(self, resultado: str):
        # TODO: Comprobar que el resultado es válido para un partido de baloncesto
        self._resultado = resultado


if __name__ == "__main__":
    partidos: [Partido] = []

    futbol1 = PartidoFutbol("2022-11-07 21:00:00", "Estadio de Vallecas", "Rayo Vallecano", "Real Madrid", puntos_victoria=3, puntos_empate=1, puntos_derrota=0)
    futbol1.dar_resultado("3-2")
    partidos.append(futbol1)
    baloncesto1 = PartidoBaloncesto("2023-02-01 20:00:00", "Palacio de los Deportes de Madrid", "Real Madrid", "Panathinaikos", puntos_victoria=1, puntos_derrota=0)
    baloncesto1.dar_resultado("83-68")
    partidos.append(baloncesto1)

    for partido in partidos:
        partido.imprimir_resumen()
