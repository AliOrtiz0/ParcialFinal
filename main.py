# ============================================================
# PROYECTO: SIMULADOR BASICO DE CAJERO AUTOMATICO 
# Autor: Ali David Ortiz Povea
# Lenguaje: Python
#
# El programa permite:
# - Iniciar sesion con el numero de cuenta.
# - Consultar el saldo.
# - Consignar dinero usando denominaciones colombianas.
# - Retirar dinero segun el saldo y el inventario disponible.
# - Consultar el historial de transacciones.
# - Guardar la informacion en archivos de texto.
# ============================================================

import os
from datetime import datetime


# ------------------------------------------------------------
# 1. CONSTANTES DEL PROGRAMA
# ------------------------------------------------------------

# Ruta de la carpeta donde se encuentra este archivo Python.
CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_USUARIOS = os.path.join(CARPETA_PROYECTO, "usuarios.txt")
ARCHIVO_INVENTARIO = os.path.join(CARPETA_PROYECTO, "inventario.txt")
ARCHIVO_HISTORIAL = os.path.join(CARPETA_PROYECTO, "historial.txt")

# Denominaciones aceptadas en Colombia, ordenadas de mayor a menor.
DENOMINACIONES = [
    100000, 50000, 20000, 10000, 5000, 2000,
    1000, 500, 200, 100, 50
]


# ------------------------------------------------------------
# 2. CREACION DE LOS ARCHIVOS INICIALES
# ------------------------------------------------------------

def crear_archivos_iniciales():
    """Crea los archivos con datos de ejemplo si todavía no existen."""

    # Se registran tres usuarios de ejemplo.
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
            archivo.write("Juan Perez|1001|500000\n")
            archivo.write("Maria Lopez|1002|750000\n")
            archivo.write("Carlos Gomez|1003|1000000\n")

    # Se registra el inventario inicial del cajero.
    if not os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
            archivo.write("100000|5\n")
            archivo.write("50000|10\n")
            archivo.write("20000|15\n")
            archivo.write("10000|20\n")
            archivo.write("5000|20\n")
            archivo.write("2000|30\n")
            archivo.write("1000|30\n")
            archivo.write("500|30\n")
            archivo.write("200|30\n")
            archivo.write("100|30\n")
            archivo.write("50|30\n")

    # Se crea el historial vacío si no existe.
    if not os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8"):
            pass


# ------------------------------------------------------------
# 3. CARGA Y GUARDADO DE USUARIOS
# ------------------------------------------------------------

def cargar_usuarios():
    """Lee los usuarios del archivo y los guarda en un diccionario."""

    usuarios = {}

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                # Cada registro debe tener nombre, cuenta y saldo.
                if len(datos) == 3:
                    nombre = datos[0]
                    numero_cuenta = datos[1]

                    try:
                        saldo = int(datos[2])

                        if saldo >= 0:
                            usuarios[numero_cuenta] = {
                                "nombre": nombre,
                                "saldo": saldo
                            }
                    except ValueError:
                        print("Se encontro un saldo no valido en usuarios.txt.")

    except FileNotFoundError:
        print("Error: No se encontro el archivo de usuarios.")

    return usuarios


def guardar_usuarios(usuarios):
    """Guarda los saldos actualizados de todos los usuarios."""

    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        for cuenta, informacion in usuarios.items():
            linea = (
                informacion["nombre"] + "|" +
                cuenta + "|" +
                str(informacion["saldo"]) + "\n"
            )
            archivo.write(linea)


# ------------------------------------------------------------
# 4. CARGA Y GUARDADO DEL INVENTARIO
# ------------------------------------------------------------

def cargar_inventario():
    """Lee las cantidades disponibles de billetes y monedas."""

    inventario = {}

    try:
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) == 2:
                    try:
                        denominacion = int(datos[0])
                        cantidad = int(datos[1])

                        if denominacion in DENOMINACIONES and cantidad >= 0:
                            inventario[denominacion] = cantidad

                    except ValueError:
                        print("Se encontro un dato no valido en inventario.txt.")

    except FileNotFoundError:
        print("Error: No se encontro el archivo de inventario.")

    # Si falta alguna denominacion en el archivo, se inicia en cero.
    for denominacion in DENOMINACIONES:
        if denominacion not in inventario:
            inventario[denominacion] = 0

    return inventario


def guardar_inventario(inventario):
    """Guarda las cantidades actuales del inventario."""

    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        for denominacion in DENOMINACIONES:
            linea = str(denominacion) + "|" + str(inventario[denominacion]) + "\n"
            archivo.write(linea)


# ------------------------------------------------------------
# 5. REGISTRO Y CONSULTA DEL HISTORIAL
# ------------------------------------------------------------

def registrar_transaccion(cuenta, nombre, tipo, valor):
    """Agrega una transaccion al archivo de historial."""

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
        archivo.write(
            fecha + "|" + cuenta + "|" + nombre + "|" +
            tipo + "|" + str(valor) + "\n"
        )


def mostrar_historial(cuenta):
    """Muestra las transacciones registradas para la cuenta indicada."""

    print("\nHISTORIAL DE TRANSACCIONES")
    encontrado = False

    try:
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) == 5 and datos[1] == cuenta:
                    print("----------------------------------------")
                    print("Fecha:", datos[0])
                    print("Usuario:", datos[2])
                    print("Operacion:", datos[3])
                    print("Valor: $", datos[4])
                    encontrado = True

        if not encontrado:
            print("No hay transacciones registradas para esta cuenta.")

    except FileNotFoundError:
        print("Error: No se encontro el archivo de historial.")


# ------------------------------------------------------------
# 6. FUNCION PARA INICIAR SESION
# ------------------------------------------------------------

def iniciar_sesion(usuarios):
    """Solicita el numero de cuenta y verifica que exista."""

    while True:
        numero_cuenta = input("\nIngrese su numero de cuenta: ").strip()

        if numero_cuenta in usuarios:
            print("\nBienvenido(a),", usuarios[numero_cuenta]["nombre"])
            return numero_cuenta

        print("Error: La cuenta no existe. Intente nuevamente.")


# ------------------------------------------------------------
# 7. CONSULTA DE SALDO
# ------------------------------------------------------------

def consultar_saldo(usuarios, cuenta):
    """Muestra el nombre, numero de cuenta y saldo del usuario."""

    print("\nCONSULTA DE SALDO")
    print("Usuario:", usuarios[cuenta]["nombre"])
    print("Numero de cuenta:", cuenta)
    print("Saldo disponible: $", usuarios[cuenta]["saldo"])


# ------------------------------------------------------------
# 8. CONSIGNACION DE DINERO
# ------------------------------------------------------------

def consignar_dinero(usuarios, inventario, cuenta):
    """Aumenta el saldo del usuario y las cantidades del inventario."""

    print("\nDENOMINACIONES ACEPTADAS")
    for denominacion in DENOMINACIONES:
        print("$", denominacion)

    try:
        denominacion = int(input("Ingrese la denominacion: "))

        if denominacion not in DENOMINACIONES:
            print("Error: Denominacion no valida.")
            return

        cantidad = int(input("Ingrese la cantidad de billetes o monedas: "))

        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor que cero.")
            return

        # Se calcula el valor total recibido.
        total = denominacion * cantidad

        # Se actualizan el saldo y el inventario.
        usuarios[cuenta]["saldo"] += total
        inventario[denominacion] += cantidad

        # Se guardan los cambios en los archivos.
        guardar_usuarios(usuarios)
        guardar_inventario(inventario)

        # Se registra la operacion en el historial.
        registrar_transaccion(
            cuenta, usuarios[cuenta]["nombre"], "Consignacion", total
        )

        print("\nCONSIGNACION EXITOSA")
        print("Valor consignado: $", total)
        print("Nuevo saldo: $", usuarios[cuenta]["saldo"])

    except ValueError:
        print("Error: Debe ingresar valores numericos.")


# ------------------------------------------------------------
# 9. CALCULO DE DENOMINACIONES PARA UN RETIRO
# ------------------------------------------------------------

def calcular_denominaciones(monto, inventario):
    """
    Busca una combinacion que entregue el monto exacto usando
    el inventario disponible y la menor cantidad de piezas.

    Se utiliza una tabla de posibilidades: para cada valor posible
    se conserva la combinacion que utiliza menos billetes o monedas.
    """

    # Todas las denominaciones son multiplos de 50.
    objetivo = monto // 50

    # La clave es el valor alcanzado en unidades de 50.
    # El contenido guarda (cantidad_total_de_piezas, combinacion).
    posibilidades = {0: (0, {})}

    for denominacion in DENOMINACIONES:
        valor = denominacion // 50
        disponibles = inventario[denominacion]
        nuevas_posibilidades = {}

        for suma_actual, informacion in posibilidades.items():
            piezas_actuales, combinacion_actual = informacion

            # Probar desde cero hasta la cantidad disponible de esta denominacion.
            maximo = min(disponibles, (objetivo - suma_actual) // valor)

            for cantidad in range(maximo + 1):
                nueva_suma = suma_actual + (cantidad * valor)
                nuevas_piezas = piezas_actuales + cantidad

                if nueva_suma > objetivo:
                    continue

                # Conservar la combinacion con menos piezas para ese valor.
                if (nueva_suma not in nuevas_posibilidades or
                        nuevas_piezas < nuevas_posibilidades[nueva_suma][0]):

                    nueva_combinacion = combinacion_actual.copy()

                    if cantidad > 0:
                        nueva_combinacion[denominacion] = cantidad

                    nuevas_posibilidades[nueva_suma] = (
                        nuevas_piezas, nueva_combinacion
                    )

        posibilidades = nuevas_posibilidades

    if objetivo in posibilidades:
        return posibilidades[objetivo][1]

    return None


# ------------------------------------------------------------
# 10. RETIRO DE DINERO
# ------------------------------------------------------------

def retirar_dinero(usuarios, inventario, cuenta):
    """Valida el saldo y el inventario antes de entregar el dinero."""

    try:
        monto = int(input("\nIngrese el valor que desea retirar: "))

        if monto <= 0:
            print("Error: El monto debe ser mayor que cero.")
            return

        if monto % 50 != 0:
            print("Error: El cajero solo puede entregar multiplos de $50.")
            return

        if monto > usuarios[cuenta]["saldo"]:
            print("Error: Saldo insuficiente.")
            return

        # Calcular la combinacion exacta con el inventario disponible.
        combinacion = calcular_denominaciones(monto, inventario)

        if combinacion is None:
            print("Error: El cajero no cuenta con las denominaciones necesarias.")
            return

        # Descontar del inventario las piezas entregadas.
        print("\nRETIRO REALIZADO")
        print("Detalle del dinero entregado:")

        for denominacion in DENOMINACIONES:
            cantidad = combinacion.get(denominacion, 0)

            if cantidad > 0:
                print("$", denominacion, "-", cantidad, "unidad(es)")
                inventario[denominacion] -= cantidad

        # Actualizar el saldo del usuario.
        usuarios[cuenta]["saldo"] -= monto

        # Guardar los cambios en los archivos.
        guardar_usuarios(usuarios)
        guardar_inventario(inventario)

        # Registrar el retiro en el historial.
        registrar_transaccion(
            cuenta, usuarios[cuenta]["nombre"], "Retiro", monto
        )

        print("Total retirado: $", monto)
        print("Saldo restante: $", usuarios[cuenta]["saldo"])

    except ValueError:
        print("Error: Debe ingresar un valor numerico.")


# ------------------------------------------------------------
# 11. MENU PRINCIPAL
# ------------------------------------------------------------

def mostrar_menu():
    """Muestra las operaciones disponibles en el cajero."""

    print("\n================================")
    print("       CAJERO AUTOMATICO")
    print("================================")
    print("1. Consultar saldo")
    print("2. Consignar dinero")
    print("3. Retirar dinero")
    print("4. Ver historial de transacciones")
    print("5. Salir")
    print("================================")


# ------------------------------------------------------------
# 12. FUNCION PRINCIPAL DEL PROGRAMA
# ------------------------------------------------------------

def ejecutar_cajero():
    """Carga los archivos, inicia sesion y controla el menu."""

    # Crear los archivos de ejemplo si no existen.
    crear_archivos_iniciales()

    # Cargar la informacion guardada.
    usuarios = cargar_usuarios()
    inventario = cargar_inventario()

    if len(usuarios) < 3:
        print("Advertencia: El archivo debe contener minimo tres usuarios.")

    if len(usuarios) == 0:
        print("No hay usuarios disponibles. Revise usuarios.txt.")
        return

    print("SIMULADOR DE CAJERO AUTOMATICO")

    # Identificar al usuario que utilizara el cajero.
    cuenta = iniciar_sesion(usuarios)

    opcion = 0

    # Repetir el menu hasta que el usuario seleccione salir.
    while opcion != 5:
        mostrar_menu()

        try:
            opcion = int(input("Seleccione una opcion: "))

            if opcion == 1:
                consultar_saldo(usuarios, cuenta)

            elif opcion == 2:
                consignar_dinero(usuarios, inventario, cuenta)

            elif opcion == 3:
                retirar_dinero(usuarios, inventario, cuenta)

            elif opcion == 4:
                mostrar_historial(cuenta)

            elif opcion == 5:
                print("Gracias por utilizar el cajero automatico.")

            else:
                print("Opcion no valida. Intente nuevamente.")

        except ValueError:
            print("Error: Debe ingresar un numero para seleccionar una opcion.")


# ------------------------------------------------------------
# 13. INICIO DEL PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":
    ejecutar_cajero()
