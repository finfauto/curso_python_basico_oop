class Persona:
    def __init__(self, nombre, apellido):
        self.__nombre = nombre
        self.__apellido = apellido

    def __del__(self):
        print(f"Soy {self.__nombre} {self.__apellido} y como ya no me necesitan me están destruyendo")

    def saludo(self):
        print(f"Hola, soy {self.__nombre} {self.__apellido}")


if __name__ == "__main__":
    persona = Persona("Alberto", "López")
    persona.saludo()
    persona = Persona("Alba", "García")
    persona.saludo()
