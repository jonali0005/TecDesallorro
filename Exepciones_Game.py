import random

# Programa: Exepciones_Game.py
# Descripción: Un juego de adivinanza de números que utiliza excepciones para validar datos.

def jugar():
    # Generamos un número aleatorio entre 1 y 20
    numero_secreto = random.randint(1, 20)
    intentos = 0
    ganado = False

    print("========================================")
    print("   ¡BIENVENIDO AL JUEGO DE ADIVINANZA!  ")
    print("========================================")
    print("He pensado un número entre 1 y 20. ¿Puedes adivinarlo?")
    print("(Presiona Ctrl+C para salir en cualquier momento)\n")

    while not ganado:
        try:
            # Pedimos el número al usuario
            entrada = input(f"Intento #{intentos + 1} - Ingresa tu número: ")
            
            # Intentamos convertir la entrada a un número entero
            # Aquí es donde puede ocurrir un ValueError
            numero_usuario = int(entrada)

            # Validación lógica: el número debe estar en el rango
            if numero_usuario < 1 or numero_usuario > 20:
                # Podríamos lanzar nuestra propia excepción, pero para mantenerlo sencillo
                # usaremos un mensaje directo, aunque el try captura errores de tipo.
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
                print(f"\n¡FELICIDADES! Adivinaste el número en {intentos} intentos.")

        except ValueError:
            # Se ejecuta si el usuario ingresa letras o símbolos en lugar de números
            print("-> Error: ¡Eso no es un número válido! Intenta ingresar solo dígitos.")
        
        except KeyboardInterrupt:
            # Se ejecuta si el usuario presiona Ctrl+C para cerrar el juego bruscamente
            print("\n\nJuego cancelado por el usuario. ¡Hasta la próxima!")
            break
        
        except Exception as e:
            # Captura cualquier otro error inesperado para que el programa no "explote"
            print(f"Ocurrió un error inesperado: {e}")
            break

if __name__ == "__main__":
    jugar()
