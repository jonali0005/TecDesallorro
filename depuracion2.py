# Programa: carrito de compras simple

carrito = {}  # Diccionario: { nombre: {precio: float, cantidad: int} }


def agregar_producto(nombre, precio, cantidad):
    # 🔥 Validación de tipos y valores
    if precio < 0 or cantidad <= 0:
        print("Precio o cantidad inválidos")
        return

    # 🔥 Si el producto ya existe, acumulamos cantidad
    if nombre in carrito:
        carrito[nombre]["cantidad"] += cantidad
    else:
        # Guardamos como números (no strings)
        carrito[nombre] = {"precio": precio, "cantidad": cantidad}

    print("Producto agregado")


def mostrar_carrito():
    print("Carrito actual:")

    if len(carrito) == 0:
        print("El carrito está vacío")
        return

    total = 0

    # 🔥 Iteramos correctamente sobre el diccionario
    for producto, datos in carrito.items():
        precio = datos["precio"]
        cantidad = datos["cantidad"]

        subtotal = precio * cantidad

        # 🔴 ERROR ORIGINAL: total =+ subtotal (sobrescribe)
        # ✅ Correcto:
        total += subtotal

        print(producto, "x", cantidad, "=", subtotal)

    print("Total:", total)


def eliminar_producto(nombre1, cantidad2):
    if nombre not in carrito:
        print("No existe el producto")
    else:
        # 🔴 ERROR ORIGINAL: faltaban paréntesis y argumento
        # carrito.pop
        # ✅ Correcto:
        carrito.pop(nombre)
        print("Producto eliminado")


while True:
    print("\n1. Agregar producto")
    print("2. Ver carrito")
    print("3. Eliminar producto")
    print("4. Salir")

    opcion = input("Selecciona una opcion: ")

    # 🔥 Validamos opción como string (más seguro para menú simple)
    if opcion == "1":
        nombre = input("Nombre: ")

        try:
            # 🔴 ERROR ORIGINAL: venían como string
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
        except ValueError:
            print("Debes ingresar valores numéricos válidos")
            continue

        agregar_producto(nombre, precio, cantidad)

    elif opcion == "2":
        mostrar_carrito()

    elif opcion == "3":
        nombre = input("Producto a eliminar: ")
        eliminar_producto(nombre)

    elif opcion == "4":  # 🔴 ERROR ORIGINAL: faltaba ':'
        print("Adios")
        break

    else:
        print("Opcion invalida")