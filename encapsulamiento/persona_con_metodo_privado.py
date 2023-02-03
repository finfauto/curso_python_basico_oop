class Persona:
    def __init__(self, nombre, apellido):
        self.__nombre = nombre
        self.__apellido = apellido

    def saludo(self):
        print(f"Hola, soy {self.__construir_nombre_completo()}")

    def __construir_nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"


if __name__ == "__main__":
    persona1 = Persona("Alberto", "López")
    persona1.saludo()
    persona1.__construir_nombre_completo()
