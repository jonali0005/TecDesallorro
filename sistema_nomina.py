# --- CLASE PADRE (ABSTRACCIÓN) ---
class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

    def calcular_pago(self):
        """Método que será sobrescrito por las clases hijas"""
        pass

# --- CLASES HIJAS (HERENCIA Y POLIMORFISMO) ---

class EmpleadoAdministrativo(Empleado):
    def __init__(self, nombre, sueldo_mensual):
        super().__init__(nombre)
        self.sueldo_mensual = sueldo_mensual

    # Polimorfismo: Implementación específica para Administrativos
    def calcular_pago(self):
        return self.sueldo_mensual

class EmpleadoPorHora(Empleado):
    def __init__(self, nombre, horas_trabajadas, tarifa_hora):
        super().__init__(nombre)
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora

    # Polimorfismo: Implementación específica para Programadores/Consultores
    def calcular_pago(self):
        return self.horas_trabajadas * self.tarifa_hora

class EmpleadoVendedor(Empleado):
    def __init__(self, nombre, sueldo_base, ventas_realizadas, comision):
        super().__init__(nombre)
        self.sueldo_base = sueldo_base
        self.ventas_realizadas = ventas_realizadas
        self.comision = comision

    # Polimorfismo: Implementación específica para Vendedores
    def calcular_pago(self):
        return self.sueldo_base + (self.ventas_realizadas * self.comision)

# --- FUNCIÓN QUE DEMUESTRA EL POLIMORFISMO ---

def procesar_nomina(empleados):
    print("--- REPORTE DE PAGOS MENSUALES ---")
    total_nomina = 0
    
    for empleado in empleados:
        # Aquí ocurre el POLIMORFISMO:
        # El código trata a todos como 'Empleado', pero llama a la versión
        # correcta de 'calcular_pago' según la clase real del objeto.
        pago = empleado.calcular_pago()
        print(f"Empleado: {empleado.nombre:<15} | Pago total: ${pago:,.2f}")
        total_nomina += pago
        
    print("-" * 45)
    print(f"TOTAL A PAGAR EN NÓMINA: ${total_nomina:,.2f}")

# --- EJECUCIÓN DEL PROGRAMA ---

if __name__ == "__main__":
    # Creamos una lista con diferentes tipos de empleados
    lista_empleados = [
        EmpleadoAdministrativo("Ana Martínez", 2500),
        EmpleadoPorHora("Carlos Ruiz", 160, 15),
        EmpleadoVendedor("Sofía López", 1200, 5000, 0.10)
    ]

    # Procesamos a todos de forma uniforme
    procesar_nomina(lista_empleados)
