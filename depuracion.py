id="p9x3k1"
# Programa: lista de tareas simple

tareas = []

def agregar_tarea(nombre):
    tareas.append(nombre)
    print("Tarea agregada")

def mostrar_tareas():
    print("Tus tareas son:")
    for i in range(len(tareas)):
        print(i + 1, tareas[i])

def eliminar_tarea(indice):
    if indice > len(tareas):
        print("Indice invalido")
    else:
        tareas.pop(indice)
        print("Tarea eliminada")

while True:
    print("\n1. Agregar tarea")
    print("2. Mostrar tareas")
    print("3. Eliminar tarea")
    print("4. Salir")

    opcion = int(input("Elige una opcion: "))

    if opcion == 1:
        nombre = input("Nombre de la tarea: ")
        agregar_tarea(nombre)

    elif opcion == 2:
        mostrar_tareas()

    elif opcion == 3:
        indice = input("Indice de la tarea a eliminar: ")
        eliminar_tarea(indice)

    elif opcion == 4:
        print("Adios")
        break

    else:
        print("Opcion invalida")