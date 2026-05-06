# Programa: sistema bancario simple

class Cuenta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

        self.saldo = 0

    def depositar(self, monto):
        if monto <= 0:
            print("Monto invalido")
        else:
            self.saldo =+ monto
            print("Deposito realizado")

    def retirar(self, monto):
        if monto > self.saldo:
            print("Fondos insuficientes")
        else:
            self.saldo = self.saldo - monto
            print("Retiro realizado")

    def mostrar_saldo(self, titular):
        print("Titular:", self.titular)
        print("Saldo:", self.saldo)


class Banco:
    def __init__(self,cuentas):
        self.cuentas = cuentas
        self.cuentas = []

    def crear_cuenta(self, titular):
        cuenta = Cuenta(titular)
        self.cuentas.append(cuenta)
        print("Cuenta creada")

    def buscar_cuenta(self, titular):
        for c in self.cuentas:
            if c.titular == titular:
                return c
        return None

    def transferir(self, origen, destino, monto):
        cuenta_origen = self.buscar_cuenta(origen)
        cuenta_destino = self.buscar_cuenta(destino)

        if cuenta_origen == None or cuenta_destino == None:
            print("Cuenta no encontrada")
        else:
            cuenta_origen.retirar(monto)
            cuenta_destino.depositar(monto)
            print("Transferencia realizada")


# --- Ejecución ---
banco = Banco()

banco.crear_cuenta("Ana")
banco.crear_cuenta("Luis")

banco.transferir("Ana", "Luis", 100)

cuenta = banco.buscar_cuenta("Luis")
cuenta.mostrar_saldo()