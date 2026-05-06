# Programa: sistema de biblioteca simple


class Libro:
    def __init__(self, titulo, autor, disponible=True):
        # Constructor de la clase Libro
        # titulo: nombre del libro
        # autor: autor del libro
        # disponible: indica si el libro puede prestarse (True por defecto)
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def prestar(self):
        # Método para prestar el libro
        # Si ya está prestado, no se puede volver a prestar
        if self.disponible == False:
            print("Libro no disponible")
            return False  # Indicamos que falló la operación
        else:
            self.disponible = False  # Cambiamos estado a "prestado"
            print("Libro prestado")
            return True  # Operación exitosa

    def devolver(self):
        # Método para devolver el libro
        # Si ya está disponible, no tiene sentido devolverlo
        if self.disponible == True:
            print("El libro ya estaba disponible")
            return False
        else:
            self.disponible = True  # Cambiamos estado a "disponible"
            print("Libro devuelto")
            return True


class Biblioteca:
    def __init__(self):
        # Lista donde se almacenan los objetos Libro
        self.libros = []

    def agregar_libro(self, libro):
        # Agrega un objeto Libro a la biblioteca
        self.libros.append(libro)

    def mostrar_libros(self):
        # Muestra todos los libros con su estado actual
        if len(self.libros) == 0:
            print("No hay libros en la biblioteca")
            return

        for libro in self.libros:
            # Usamos operador ternario para mostrar estado
            estado = "Disponible" if libro.disponible else "Prestado"
            print(libro.titulo, "-", estado)

    def prestar_libro(self, titulo):
        # Busca un libro por título y lo presta
        for libro in self.libros:
            if libro.titulo == titulo:
                # Llama al método del objeto Libro
                libro.prestar()
                return  # Salimos después de encontrarlo
        print("Libro no encontrado")

    def devolver_libro(self, titulo):
        # Busca un libro por título y lo devuelve
        for libro in self.libros:
            if libro.titulo == titulo:
                libro.devolver()
                return
        print("Libro no encontrado")


# ----------------------------
# Ejecución del programa
# ----------------------------

# Creamos una instancia de Biblioteca
biblio = Biblioteca()

# Creamos dos libros (objetos de la clase Libro)
libro1 = Libro("1984", "Orwell")
libro2 = Libro("Dune", "Herbert")

# Agregamos los libros a la biblioteca
biblio.agregar_libro(libro1)
biblio.agregar_libro(libro2)

# Mostramos el estado inicial
biblio.mostrar_libros()

# Prestamos un libro
biblio.prestar_libro("1984")

# Mostramos estado después del préstamo
biblio.mostrar_libros()

# Devolvemos el libro
biblio.devolver_libro("1984")

# Mostramos estado final
biblio.mostrar_libros()