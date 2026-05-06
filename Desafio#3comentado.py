# Importamos Counter desde collections
# Counter es una estructura tipo diccionario que cuenta automáticamente
# cuántas veces aparece cada elemento en un iterable (en este caso, letras)
from collections import Counter


# Definimos la clase Genetica
class Genetica:

    # Método constructor: se ejecuta cuando creamos un objeto
    def __init__(self, palabra):
        # Convertimos la palabra a minúsculas para evitar duplicados
        # como 'A' y 'a' (se consideran iguales)
        self.palabra = palabra.upper()


    # Método que genera el "ADN" (formato letra + frecuencia)
    def generar_adn(self):

        # Counter recorre toda la palabra y crea un diccionario
        # Ejemplo: "aaabbc" → {'a':3, 'b':2, 'c':1}
        conteo = Counter(self.palabra)

        # Variable donde construiremos el resultado final
        resultado = ""

        # Conjunto (set) para guardar letras que ya procesamos
        # Sirve para evitar repetir letras en el resultado
        letras_vistas = set()

        # Recorremos la palabra ORIGINAL (esto mantiene el orden)
        for letra in self.palabra:

            # Si la letra NO ha sido usada antes
            if letra not in letras_vistas:

                # Agregamos al resultado:
                # - la letra actual
                # - su frecuencia (usando Counter)
                # Ejemplo: 'a' + 3 → "a3"
                resultado += f"{letra}{conteo[letra]}"

                # Marcamos la letra como ya usada
                letras_vistas.add(letra)

        # Regresamos el string final
        return resultado


    # Método para imprimir directamente el ADN
    def imprimir_adn(self):

        # Llama al método generar_adn() y muestra el resultado en consola
        print(self.generar_adn())


# Cadena de entrada (simula un "ADN")
New_ADN = 'sjjdfjsjrjsjfjdrj '

# Creamos un objeto de la clase Genetica
# Se ejecuta __init__ automáticamente
NEW = Genetica(New_ADN)

# Llamamos al método para imprimir el ADN procesado
NEW.imprimir_adn()