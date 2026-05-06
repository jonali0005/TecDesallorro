from collections import Counter

palabra = "programacion"
conteo = Counter(palabra)

resultado = ""
letras_vistas = set()

for letra in palabra:
    if letra not in letras_vistas:
        resultado += f"{letra}{conteo[letra]}"
        letras_vistas.add(letra)

print(resultado)