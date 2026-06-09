import random
import time
import json
import os

# Programa: Exepciones_Game.py
# Descripción: Un juego de adivinanza de números mejorado con ranking en JSON y medición de tiempo.

# Definir la ruta del archivo de ranking en la misma carpeta que el script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RANKING_FILE = os.path.join(SCRIPT_DIR, "ranking.json")

def cargar_ranking():
    """Carga el ranking desde un archivo JSON."""
    if os.path.exists(RANKING_FILE):
        try:
            with open(RANKING_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def guardar_ranking(nombre, tiempo, intentos):
    """Actualiza el ranking con el nuevo resultado y lo guarda en el archivo JSON."""
    ranking = cargar_ranking()
    ranking.append({
        "nombre": nombre,
        "tiempo": round(tiempo, 2),
        "intentos": intentos
    })
    # Ordenar por tiempo (menor a mayor)
    ranking.sort(key=lambda x: x["tiempo"])
    # Mantener solo los mejores 5
    ranking = ranking[:5]
    
    try:
        with open(RANKING_FILE, "w") as f:
            json.dump(ranking, f, indent=4)
        print("\n¡Tu record ha sido guardado en el ranking!")
    except IOError as e:
        print(f"\nError al guardar el ranking: {e}")
    
    return ranking

def mostrar_ranking():
    """Muestra el ranking actual en pantalla."""
    ranking = cargar_ranking()
    if not ranking:
        print("\n--- No hay records registrados todavía ---")
        return
    
    print("\n========================================")
    print("        TOP 5 - MEJORES TIEMPOS        ")
    print("========================================")
    print(f"{'Pos':<4} {'Nombre':<15} {'Tiempo':<10} {'Intentos'}")
    print("-" * 40)
    for i, entry in enumerate(ranking, 1):
        print(f"{i:<4} {entry['nombre']:<15} {entry['tiempo']:<10} {entry['intentos']}")
    print("========================================\n")

def jugar():
    # Generamos un número aleatorio entre 1 y 20
    numero_secreto = random.randint(1, 20)
    intentos = 0
    ganado = False

    print("========================================")
    print("   ¡BIENVENIDO AL JUEGO DE ADIVINANZA!  ")
    print("========================================")
    
    # Pedir nombre al jugador
    nombre_jugador = input("Antes de empezar, ¿cuál es tu nombre?: ").strip()
    if not nombre_jugador:
        nombre_jugador = "Jugador Anónimo"

    print(f"\nHola {nombre_jugador}, he pensado un número entre 1 y 20.")
    print("¿Puedes adivinarlo en el menor tiempo posible?")
    print("(Presiona Ctrl+C para salir en cualquier momento)\n")

    # Iniciar cronómetro
    tiempo_inicio = time.time()

    while not ganado:
        try:
            # Pedimos el número al usuario
            entrada = input(f"Intento #{intentos + 1} - Ingresa tu número: ")
            
            # Intentamos convertir la entrada a un número entero
            numero_usuario = int(entrada)

            # Validación lógica: el número debe estar en el rango
            if numero_usuario < 1 or numero_usuario > 20:
                print("-> Error: Por favor, elige un número que esté entre 1 y 20.")
                continue

            intentos += 1

            # Comprobamos si el usuario acertó
            if numero_usuario < numero_secreto:
                print("Demasiado bajo. ¡Intenta otra vez!")
            elif numero_usuario > numero_secreto:
                print("Demasiado alto. ¡Intenta otra vez!")
            else:
                ganado = True
                tiempo_final = time.time()
                tiempo_total = tiempo_final - tiempo_inicio
                
                print(f"\n¡FELICIDADES {nombre_jugador.upper()}!")
                print(f"Adivinaste el número en {intentos} intentos.")
                print(f"Tiempo total: {tiempo_total:.2f} segundos.")
                
                # Guardar en ranking
                guardar_ranking(nombre_jugador, tiempo_total, intentos)
                # Mostrar ranking actualizado
                mostrar_ranking()

        except ValueError:
            print("-> Error: ¡Eso no es un número válido! Intenta ingresar solo dígitos.")
        
        except KeyboardInterrupt:
            print("\n\nJuego cancelado por el usuario. ¡Hasta la próxima!")
            break
        
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break

if __name__ == "__main__":
    jugar()
