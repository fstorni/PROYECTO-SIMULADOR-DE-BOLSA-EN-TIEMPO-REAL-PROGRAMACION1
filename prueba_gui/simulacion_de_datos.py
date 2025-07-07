import random
import json
import os
import time

def contar_chistes(chistes, i=None):
    if i is None:
        i = len(chistes) - 1
    if i < 0:
        return
    print("Chiste " + str(len(chistes) - i) + ": " + chistes[i])
    contar_chistes(chistes, i - 1)

def pide_datos_del_usuario():
    condicion = False
    while not condicion:
        nombre = input("Escriba su nombre: ")
        try:
            edad = int(input("Ingrese su edad: "))
        except ValueError:
            print("Por favor ingrese un número")
            continue
        if nombre.isalpha():
            condicion = True
        else:
            print("Por favor ingrese un nombre que contenga solo letras")
    return nombre, edad

def crea_matriz():
    return [[0 for _ in range(4)] for _ in range(4)]

def nombres_de_empresas():
    return ["samsung", "IBM", "Mercado_libre", "Amazon"]

def rellena(matriz, empresas):
    for f in range(len(matriz)):
        matriz[f][0] = empresas[f]
        precio = 500 + random.uniform(-50, 50)
        for c in range(1, len(matriz[0])):
            variacion = random.uniform(-5, 5)
            nuevo_valor = precio + variacion
            precio = (precio + nuevo_valor) / 2
            if precio < 1:
                precio = 1
            matriz[f][c] = round(precio, 2)
    return matriz

def impresion(matriz, resultado):
    print()
    print("========== VALORES DE LAS ACCIONES ==========")
    for elementos in matriz:
        print(elementos)
    print()
    print("Promedio de las acciones cambia en cada vuelta")
    print("Estas acciones representan la tendencia de un día promediado")
    print("Comprás cierta cantidad a un valor actual y en la próxima vuelta esa misma cantidad puede valer más o menos según cómo fluctúe el mercado")
    for fila in resultado:
        print(f"{fila[0].upper()} --> {fila[1]:.2f} --> Precio promedio")
    print("==============================================")
    print()

def calcular_promedios(matriz):
    return [(fila[0], sum(fila[1:])/3) for fila in matriz]

def actualizar_valores(empresas):
    matriz = crea_matriz()
    matriz = rellena(matriz, empresas)
    promedios = calcular_promedios(matriz)
    return matriz, {empresa: promedio for empresa, promedio in promedios}

def mostrar_portafolio(saldo, portafolio, precios, precios_anteriores):
    print()
    print("----- TU PORTAFOLIO -----")
    print(f"Saldo disponible: ${saldo:.2f}")
    for empresa, info in portafolio.items():
        acciones = info["acciones"]
        valor_actual = acciones * precios[empresa]
        valor_anterior = acciones * precios_anteriores.get(empresa, precios[empresa])
        diferencia = valor_actual - valor_anterior
        signo = "+" if diferencia > 0 else ""
        cambio_str = f"{signo}{diferencia:.2f}"
        print(f"{empresa}: ${valor_actual:.2f} ganancia o pérdida respecto a vuelta anterior {cambio_str} acciones: {acciones:.2f} invertido: ${info['inversion']:.2f}")
    print("-------------------------")
    print()

def retirar(empresa, saldo, portafolio, precios):
    acciones_disponibles = portafolio[empresa]["acciones"]
    if acciones_disponibles <= 0:
        print("No tenés acciones en esa empresa")
        return saldo, 0, 0

    print(f"Tenés {acciones_disponibles:.2f} acciones en {empresa}")
    condicion = False
    porcentaje = 0

    while not condicion:
        entrada = input("¿Qué porcentaje querés retirar? 0 a 100 o -1 para cancelar: ")
        try:
            porcentaje = float(entrada)
        except:
            print("Porcentaje inválido")
        else:
            if porcentaje == -1:
                print("Operación cancelada")
                return saldo, 0, 0
            if 0 < porcentaje <= 100:
                condicion = True
            else:
                print("Porcentaje fuera de rango. Intentá de nuevo o poné -1 para cancelar")

    acciones_a_retirar = (porcentaje / 100) * acciones_disponibles
    precio_actual = precios[empresa]
    monto_retirado = acciones_a_retirar * precio_actual
    inversion_unitaria = portafolio[empresa]["inversion"] / acciones_disponibles
    inversion_parcial = acciones_a_retirar * inversion_unitaria
    ganancia = monto_retirado - inversion_parcial

    portafolio[empresa]["acciones"] -= acciones_a_retirar
    portafolio[empresa]["inversion"] -= inversion_parcial
    saldo += monto_retirado

    if inversion_parcial > 0:
        variacion = (ganancia / inversion_parcial) * 100
    else:
        variacion = 0

    print(f"Retiraste el {porcentaje:.2f}% de tus acciones {acciones_a_retirar:.2f} en {empresa} por ${monto_retirado:.2f} ganancia: {ganancia:.2f} variación: {variacion:.2f}%")
    return saldo, ganancia, inversion_parcial

def elegir_empresa_valida(empresas):
    while True:
        print("------ EMPRESAS DISPONIBLES ------")
        for i, empresa in enumerate(empresas):
            print(i, "-", empresa)
        print("----------------------------------")
        entrada = input("Elegir empresa por número o -1 para salir: ")
        if entrada == "-1":
            return -1
        try:
            indice = int(entrada)
            if 0 <= indice < len(empresas):
                return indice
            else:
                print("Empresa inválida. Intentá de nuevo")
        except ValueError:
            print("Entrada inválida")

def procesar_accion(empresa, saldo, portafolio, precios):
    valida = False
    while not valida:
        print()
        print("--- OPERACIÓN EN: " + empresa.upper() + " ---")
        accion = input("¿Invertir o retirar? i o r: ").lower()
        ganancia = 0
        inversion = 0

        if accion == "i":
            if saldo == 0:
                print("No tenés saldo para invertir")
                continue

            valida_monto = False
            while not valida_monto:
                try:
                    monto = int(input("¿Cuánto dinero?: "))
                except ValueError:
                    print("Monto inválido")
                    continue

                if monto < 0:
                    print("No se puede invertir un monto negativo")
                elif monto > saldo:
                    print(f"No tenés saldo suficiente - SALDO = ${saldo:.2f}")
                elif monto > 9000:
                    confirmar = input(f"¿Estás seguro que querés invertir ${monto}? Tal vez estás poniendo mucho en una sola empresa. s o n: ").lower()
                    if confirmar == "s":
                        valida_monto = True
                    else:
                        print("Operación cancelada")
                else:
                    valida_monto = True

            saldo -= monto
            precio_actual = precios[empresa]
            acciones_compradas = monto / precio_actual
            portafolio[empresa]["inversion"] += monto
            portafolio[empresa]["acciones"] += acciones_compradas
            print(f"Invertiste ${monto} en {empresa} comprando {acciones_compradas:.2f} acciones")
            print(f"Esto representa un valor promedio de ${precio_actual:.2f} por acción en esta jornada")
            inversion = monto
            valida = True

        elif accion == "r":
            saldo, ganancia, inversion = retirar(empresa, saldo, portafolio, precios)
            if inversion > 0 or ganancia != 0:
                valida = True
            else:
                print("Intentá con otra empresa")
        else:
            print("Opción no válida")

    print("--- Fin de la operación ---")
    print()
    return saldo, ganancia, inversion

def interaccion_con_terminal(empresas):

    saldo = 10000  # SOLO se define UNA VEZ
    portafolio = {empresa: {"inversion": 0, "acciones": 0} for empresa in empresas}
    precios_anteriores = {empresa: 500 for empresa in empresas}
    inversion_total = 0
    ganancia_total = 0
    inicio = time.time()
    condicion = False

    while not condicion:
        if time.time() - inicio >= 600:
            print("Tiempo agotado")
            condicion = True
            continue

        sin_acciones = all(info["acciones"] == 0 for info in portafolio.values())

        if saldo == 0 and not sin_acciones:
            print("No tenes saldo disponible pero tenes acciones en tu portafolio")
            print("Queres continuar retirando o salir del programa")
            decision = input("Ingresa -1 para salir o cualquier otra tecla para continuar retirando: ")
            if decision == "-1":
                print("Fin del programa")
                condicion = True
                continue

        elif saldo == 0 and sin_acciones:
            print("No tenes saldo ni inversiones para operar")
            condicion = True
            continue

        matriz, precios = actualizar_valores(empresas)
        impresion(matriz, list(precios.items()))
        mostrar_portafolio(saldo, portafolio, precios, precios_anteriores)
        precios_anteriores = precios.copy()
        indice = elegir_empresa_valida(empresas)

        if indice == -1:
            print("Fin del programa")
            condicion = True
        else:
            empresa = empresas[indice]
            saldo, ganancia, inversion = procesar_accion(empresa, saldo, portafolio, precios)
            ganancia_total += ganancia
            inversion_total += inversion

    print()
    print("=== PROGRAMA FINALIZADO ===")
    mostrar_portafolio(saldo, portafolio, precios, precios_anteriores)
    print()
    print("==== RESUMEN DE GANANCIA TOTAL ====")
    print(f"Inversión total: ${inversion_total:.2f}")
    print(f"Ganancia neta: ${ganancia_total:.2f}")

    valor_total_actual = saldo
    for empresa in portafolio:
        acciones = portafolio[empresa]["acciones"]
        valor_total_actual += acciones * precios[empresa]

    diferencia = valor_total_actual - 10000
    variacion_total = (diferencia / 10000) * 100

    print(f"Valor final total: ${valor_total_actual:.2f}")
    print(f"Variacion total respecto al saldo inicial: {variacion_total:.2f}%")
    print("===================================")
    print()
    print("=== CONSEJO DE INVERSION ===")
    if diferencia > 10:
        print("Excelente resultado Lograste una ganancia sobre el valor total")
    elif diferencia < -10:
        print("Tu inversion general tuvo perdidas Revisa tu estrategia o diversifica mejor")
    else:
        print("Terminaste con un valor muy similar al inicial Quiza sea buen momento para ajustar tu estrategia")

def main():
    nombre, edad = pide_datos_del_usuario()
    print()
    print(f"Bienvenido o bienvenida {nombre} de {edad} años")
    print()
    empresas = nombres_de_empresas()
    interaccion_con_terminal(empresas)
    chistes = [
        "Por qué Python no va al gimnasio Porque ya tiene clases y objetos",
        "Qué hace un programador cuando tiene sueño Ejecuta un thread y se duerme",
        "Qué hace una función recursiva cuando se queda sola Se llama a sí misma",
        "Cuál es el colmo de un programador Tener un hijo con excepción y no poder atraparlo"
    ]
    print()
    print("Fin del simulador. Ahora algunos chistes")
    contar_chistes(chistes)

if __name__ == "__main__":
    main()
