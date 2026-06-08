# Programa: Practica_De_Exepciones.py
# Descripción: Ejemplos sencillos de manejo de excepciones en Python

def ejemplo_division_por_cero():
    """Maneja el error cuando se intenta dividir un número entre cero."""
    print("\n--- Ejemplo 1: División por Cero ---")
    try:
        numero = 10
        divisor = 0
        resultado = numero / divisor
        print(f"El resultado es: {resultado}")
    except ZeroDivisionError:
        # Se ejecuta si ocurre una división entre cero
        print("Error: No se puede dividir por cero.")

def ejemplo_valor_invalido():
    """Maneja el error cuando se intenta convertir una cadena no numérica a entero."""
    print("\n--- Ejemplo 2: Valor Inválido ---")
    try:
        # Intentamos convertir un texto que no es un número
        texto = "hola"
        numero = int(texto)
        print(f"El número es: {numero}")
    except ValueError:
        # Se ejecuta si la conversión falla
        print("Error: No se pudo convertir el texto a número. Asegúrate de usar dígitos.")

def ejemplo_archivo_no_encontrado():
    """Maneja el error cuando se intenta abrir un archivo que no existe."""
    print("\n--- Ejemplo 3: Archivo No Encontrado ---")
    try:
        # Intentamos abrir un archivo inexistente
        with open("archivo_que_no_existe.txt", "r") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        # Se ejecuta si el archivo no se encuentra en la ruta especificada
        print("Error: El archivo solicitado no existe.")

def ejemplo_completo_con_finally():
    """Muestra el uso de 'else' y 'finally'."""
    print("\n--- Ejemplo 4: Bloques Else y Finally ---")
    try:
        # Pedimos un número al usuario (simulado aquí con una variable)
        entrada = "5"
        numero = int(entrada)
        resultado = 100 / numero
    except (ValueError, ZeroDivisionError) as e:
        # Maneja múltiples errores y captura el mensaje original en 'e'
        print(f"Ocurrió un error: {e}")
    else:
        # Se ejecuta SOLO SI NO hubo ninguna excepción en el bloque try
        print(f"Operación exitosa. El resultado es: {resultado}")
    finally:
        # Se ejecuta SIEMPRE, haya ocurrido un error o no
        # Ideal para cerrar archivos o conexiones a bases de datos
        print("Finalizando el bloque de control... (Esto siempre se imprime)")

def main():
    """Función principal para ejecutar los ejemplos."""
    print("Iniciando práctica de manejo de excepciones en Python")
    
    ejemplo_division_por_cero()
    ejemplo_valor_invalido()
    ejemplo_archivo_no_encontrado()
    ejemplo_completo_con_finally()
    
    print("\nFin del programa.")

if __name__ == "__main__":
    main()
