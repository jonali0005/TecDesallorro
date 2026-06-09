import random
# --- CONCEPTO: CLASE ---
# La clase es el molde o plantilla. Aquí definimos qué es un 'Animal' en general.
class Animal:
    def __init__(self, nombre, especie):
        # --- CONCEPTO: ENCAPSULAMIENTO ---
        # Usamos '__' para hacer los atributos privados. 
        # No se pueden modificar directamente desde fuera de la clase (protección de datos).
        self.__nombre = nombre  
        self.__especie = especie
        self.__energia = 100    

    # --- CONCEPTO: MÉTODOS (Getters) ---
    # Como los atributos son privados, creamos métodos para acceder a ellos de forma segura.
    def obtener_nombre(self):
        return self.__nombre

    def obtener_energia(self):
        return self.__energia

    # --- CONCEPTO: MÉTODOS (Comportamiento) ---
    def comer(self):
        self.__energia += 20
        print(f"🍖 {self.__nombre} está comiendo. Energía: {self.__energia}")

    # Este método se define aquí pero se comportará distinto en cada animal.
    def hacer_sonido(self):
        pass
# --- CONCEPTO: HERENCIA ---
# 'Leon' hereda de 'Animal'. Obtiene sus atributos y métodos automáticamente.
class Leon(Animal):
    def __init__(self, nombre):
        # 'super()' llama al constructor de la clase padre (Animal)
        super().__init__(nombre, "León")
    # --- CONCEPTO: POLIMORFISMO ---
    # Sobrescribimos el método 'hacer_sonido'. El León tiene su propia forma de "sonar".
    def hacer_sonido(self):
        return "¡ROOOAR! 🦁"
class Loro(Animal):
    def __init__(self, nombre):
        super().__init__(nombre, "Loro")
    # POLIMORFISMO: El Loro también tiene su propia implementación de 'hacer_sonido'.
    def hacer_sonido(self):
        return "¡Quiere cacao! 🦜"
class Serpiente(Animal):
    def __init__(self, nombre):
        super().__init__(nombre, "Serpiente")
    # POLIMORFISMO: Diferente forma, mismo nombre de método.
    def hacer_sonido(self):
        return "Ssssss... 🐍"
# --- CONCEPTO: CLASE (Gestora) ---
class Zoologico:
    def __init__(self):
        # Esta lista guardará los OBJETOS que vayamos creando.
        self.animales = []
    def agregar_animal(self, animal):
        self.animales.append(animal)
        print(f"✅ {animal.obtener_nombre()} ha sido registrado en el zoo.")
    def mostrar_concierto(self):
        print("\n--- CONCIERTO DEL ZOO ---")
        for animal in self.animales:
            # Aquí se aplica el POLIMORFISMO en su máximo esplendor:
            # Tratamos a todos como 'Animal', pero cada uno responde con su propio sonido.
            print(f"{animal.obtener_nombre()} dice: {animal.hacer_sonido()}")
# --- EJECUCIÓN E INTERACCIÓN ---
def simular_zoo():
    # --- CONCEPTO: OBJETO ---
    # 'mi_zoo' es una instancia (objeto) de la clase Zoologico.
    mi_zoo = Zoologico()
    # Creamos más OBJETOS (Instancias de las subclases)
    simba = Leon("Simba")
    pepe = Loro("Pepe")
    kaa = Serpiente("Kaa")
    # Usamos los métodos del objeto 'mi_zoo'
    mi_zoo.agregar_animal(simba)
    mi_zoo.agregar_animal(pepe)
    mi_zoo.agregar_animal(kaa)
    while True:
        print("\n--- MENÚ INTERACTIVO ---")
        print("1. Escuchar a los animales (Polimorfismo)")
        print("2. Alimentar a un animal al azar (Encapsulamiento)")
        print("3. Salir")  
        opcion = input("Elige una opción: ")
        if opcion == "1":
            mi_zoo.mostrar_concierto()
        elif opcion == "2":
            # Seleccionamos un objeto animal de la lista y llamamos a su método comer
            animal_azar = random.choice(mi_zoo.animales)
            animal_azar.comer()
        elif opcion == "3":
            print("Cerrando el zoológico. ¡Adiós!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")
if __name__ == "__main__":
    simular_zoo()