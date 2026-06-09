from collections import Counter

class Genetica:

    def __init__(self, secuencia):
        self.secuencia = secuencia.lower()

    def comprimir(self):
        conteo = Counter(self.secuencia)
        resultado = ""
        letras_vistas = set()

        for letra in self.secuencia:
            if letra not in letras_vistas:
                resultado += f"{letra}{conteo[letra]}"
                letras_vistas.add(letra)

        return resultado

    def imprimir_adn(self):
        print(self.comprimir())

New_ADN = 'jhjhggfftdsffddededededdrddeddededededhbnmm'
NEW = Genetica(New_ADN)

NEW.imprimir_adn()