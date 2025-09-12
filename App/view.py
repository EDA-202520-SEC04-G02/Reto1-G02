import sys

# Importaciones necesarias
import App.logic as logic # Portar logic porque, pues muy dificil sin logic no?
from tabulate import tabulate # Para imprimir tablas bonitas
import os
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
# -------------------------------------------------

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO DONE: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control): # Note que control es el catalog en view
    """
    Carga los datos
    """
    taxisfile = data_dir + "taxis-large.csv"           # Contruimos las rutas de los archivos aquí
    neighfile = data_dir + "nyc-neighborhoods.csv"     # Así no hay que importarlos en logic, que es más limpio
    #TODO DONE: Realizar la carga de datos
    resultados = logic.load_data(control, taxisfile, neighfile) # Ahora si me voy a logic a cargar los datos, retorno los resultados
    
    print("\n=== Resultados de la carga de datos ===")
    print(f"Tiempo de carga: {resultados['time_ms']:.2f} ms")
    print(f"Total de trayectos cargados: {resultados['total_trips']}")

    # Trayecto mínimo
    min_t = resultados["min_trip"]
    print("\nTrayecto de menor distancia (>0):")
    print(f"Inicio: {min_t['pickup_datetime']} | Distancia: {min_t['trip_distance']} millas | Total: {min_t['total_amount']} USD")

    # Trayecto máximo
    max_t = resultados["max_trip"]
    print("\nTrayecto de mayor distancia:")
    print(f"Inicio: {max_t['pickup_datetime']} | Distancia: {max_t['trip_distance']} millas | Total: {max_t['total_amount']} USD")

    # Preview
    print("\nPrimeros y últimos 5 trayectos:")
    headers = ["pickup_datetime", "dropoff_datetime", "duration_min", "distance_miles", "total_amount"]
    table = [[p[h] for h in headers] for p in resultados["preview"]] # Con ayuda de char hicimos esta lista de listas para poder usar tabulate
    print(tabulate(table, headers=headers, tablefmt="grid"))
    return resultados


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO NO HACER: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 1
    
    n = int(input("Ingrese la cantidad de pasajeros a filtrar: ")) # Pedimos cantidad de pasajeros
    result = logic.req_1(control, n) # Entramos a logic para sacar los resultados del requerimiento 1

    print("\n=== Resultados Requerimiento 1 ===")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Total de trayectos filtrados: {result['total_filtered']}")

    headers = [
        "Duración prom (min)",
        "Costo prom (USD)",
        "Distancia prom (mi)",
        "Peajes prom (USD)",
        "Propina prom (USD)",
        "Medio de pago",
        "Fecha más frec"
    ]

    
    table = [[
        f"{result['avg_duration_min']:.2f}",
        f"{result['avg_cost_usd']:.2f}",
        f"{result['avg_distance_miles']:.2f}",
        f"{result['avg_tolls_usd']:.2f}",
        f"{result['avg_tips_usd']:.2f}",
        result['most_used_payment'],
        result['most_frequent_date']
    ]]
    print(tabulate(table, headers=headers, tablefmt="grid")) # De nuevo tabulate, con un poco de ayuda de ChatGPT para formatear los números


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 2
    
    payment = input("Ingrese el método de pago a filtrar (ej: CASH, CREDIT_CARD): ").strip().upper()
    result = logic.req_2(control, payment)

    print("\n=== Resultados Requerimiento 2 ===")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Total de trayectos con pago {payment}: {result['total_filtered']}")

    if result["total_filtered"] > 0:
        from tabulate import tabulate
        headers = [
            "Duración prom (min)",
            "Costo prom (USD)",
            "Distancia prom (mi)",
            "Peajes prom (USD)",
            "Propina prom (USD)",
            "Pasajeros más frec.",
            "Fecha fin más frec."
        ]
        table = [[
            f"{result['avg_duration_min']:.2f}",
            f"{result['avg_cost_usd']:.2f}",
            f"{result['avg_distance_miles']:.2f}",
            f"{result['avg_tolls_usd']:.2f}",
            f"{result['avg_tips_usd']:.2f}",
            result['most_used_passenger'],
            result['most_frequent_date']
        ]]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No se encontraron trayectos con ese método de pago.")

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 3
    min_cost = float(input("Ingrese el valor mínimo del costo total: "))
    max_cost = float(input("Ingrese el valor máximo del costo total: "))
    result = logic.req_3(control, min_cost, max_cost)

    print("\n=== Resultados Requerimiento 3 ===")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Total de trayectos en rango {min_cost}-{max_cost} USD: {result['total_filtered']}")

    if result["total_filtered"] > 0:
        from tabulate import tabulate
        headers = [
            "Duración prom (min)",
            "Costo prom (USD)",
            "Distancia prom (mi)",
            "Peajes prom (USD)",
            "Propina prom (USD)",
            "Pasajeros más frec.",
            "Fecha fin más frec."
        ]
        table = [[
            f"{result['avg_duration_min']:.2f}",
            f"{result['avg_cost_usd']:.2f}",
            f"{result['avg_distance_miles']:.2f}",
            f"{result['avg_tolls_usd']:.2f}",
            f"{result['avg_tips_usd']:.2f}",
            result['most_used_passenger'],
            result['most_frequent_date']
        ]]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No se encontraron trayectos en ese rango de costos.")

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 4
    filtro = input("Ingrese el filtro (MAYOR o MENOR): ").strip().upper() # Primero vemos si tomamos mayor o menor
    fecha_ini = input("Ingrese la fecha inicial (YYYY-MM-DD): ") # fecha in
    fecha_fin = input("Ingrese la fecha final (YYYY-MM-DD): ") # fecha out

    result = logic.req_4(control, filtro, fecha_ini, fecha_fin) # pasamos a logic

    print("\n=== Resultados Requerimiento 4 ===") # Imprimimos
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Filtro: {result['filtro']}")
    print(f"Total de trayectos en rango: {result['total_trips']}")

    if result["combo"]: # Esto es jargon de tabulate
        c = result["combo"]
        from tabulate import tabulate
        headers = ["Barrio origen", "Barrio destino", "Distancia prom (mi)", "Duración prom (min)", "Costo prom (USD)"]
        table = [[c["origen"], c["destino"], f"{c['avg_dist']:.2f}", f"{c['avg_dur']:.2f}", f"{c['avg_cost']:.2f}"]]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No se encontraron combinaciones de barrios en el rango dado.")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 5
    filtro = input("Seleccione filtro (MAYOR/MENOR): ").upper()
    fecha_ini = input("Ingrese fecha inicial (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese fecha final (YYYY-MM-DD): ")

    result = logic.req_5(control, filtro, fecha_ini, fecha_fin)

    if result["franja"] is None:
        print("No se encontraron viajes en el rango dado.")
    else:
        franja = result["franja"]
        headers = ["Franja", "Prom. Costo (USD)", "N. Viajes", "Prom. Duración (min)", "Prom. Pasajeros", "Máx. Costo", "Mín. Costo"]
        table = [[
            franja["franja"],
            round(franja["avg_cost"], 2),
            franja["count"],
            round(franja["avg_dur"], 2),
            round(franja["avg_pass"], 2),
            round(franja["max_cost"], 2),
            round(franja["min_cost"], 2)
        ]]
        print(f"\nTiempo de ejecución: {result['time_ms']} ms")
        print(f"Filtro aplicado: {result['filtro']}")
        print(f"Total de viajes procesados: {result['total_trips']}")
        print(tabulate(table, headers=headers, tablefmt="grid"))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO NO HACER: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO NO HACER: Imprimir el resultado del requerimiento 8
    pass


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main(): # Primera función que se ejecuta al ejecutar el main.py, aquí se desplegan las funciones para el usuario.
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1: # Cargar información, es la opción 1
            print("Cargando información de los archivos ....\n")
            resultados = load_data(control) # Se llama la función load_data que carga los datos y muestra los resultados
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
