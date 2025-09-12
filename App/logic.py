import time

# Imports necesarios
import csv # Para cargar los datos
from DataStructures.List import array_list as lt # Importo mi implementación de lista para guardar la información
csv.field_size_limit(2147483647) # Consejo de la guía
from datetime import datetime # Importamos datetime, porque es MUCHO MEJOR para manejar fechas que hacer todo a mano
# -----------------------------------------

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO DONE: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "trips": None,          # Lista de trayectos
        "neighborhoods": None   # Lista de barrios
    }
    
    catalog["trips"] = lt.new_list()
    catalog["neighborhoods"] = lt.new_list()
    
    return catalog


# Funciones para la carga de datos

def load_data(catalog, taxisfile, neighfile):
    """
    Carga los datos del reto
    """
    # TODO DOING: Realizar la carga de datos
    
    start = get_time()

    # Cargar trayectos
    with open(taxisfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f)
        for row in input_file:
            lt.add_last(catalog["trips"], row)

    # Cargar barrios
    with open(neighfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f)
        for row in input_file:
            lt.add_last(catalog["neighborhoods"], row)

    end = get_time()
    delta = delta_time(start, end)

    # Procesar min/max y preview
    min_trip, max_trip = find_min_max_trip(catalog["trips"])
    preview = get_preview_trips(catalog["trips"], 5)

    return {
        "time_ms": delta,
        "total_trips": lt.size(catalog["trips"]),
        "min_trip": min_trip,
        "max_trip": max_trip,
        "preview": preview
    }

# Funciones de ayuda

def trip_duration_minutes(trip):
    """
    Calcula la duración en minutos de un trayecto
    """
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        pickup = datetime.strptime(trip["pickup_datetime"], fmt)
        dropoff = datetime.strptime(trip["dropoff_datetime"], fmt)
        return (dropoff - pickup).total_seconds() / 60
    except Exception:
        return 0.0


def find_min_max_trip(trips):
    """
    Encuentra el trayecto de menor y mayor distancia (distancia > 0)
    """
    min_trip = None
    max_trip = None
    size = lt.size(trips)
    for i in range(size): 
        t = lt.get_element(trips, i)
        try:
            dist = float(t["trip_distance"])
            if dist > 0:
                if min_trip is None or dist < float(min_trip["trip_distance"]):
                    min_trip = t
                if max_trip is None or dist > float(max_trip["trip_distance"]):
                    max_trip = t
        except Exception:
            continue
    return min_trip, max_trip


def get_preview_trips(trips, n=5):
    """
    Retorna los primeros y últimos n trayectos con los campos requeridos
    """
    preview = []
    size = lt.size(trips)

    # Primeros n
    for i in range(min(n, size)):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t))

    # Últimos n
    for i in range(max(size - n, 0), size):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t))

    return preview


def format_trip(t):
    """
    Formatea un trayecto en dict con solo los campos necesarios
    """
    return {
        "pickup_datetime": t["pickup_datetime"],
        "dropoff_datetime": t["dropoff_datetime"],
        "duration_min": round(trip_duration_minutes(t), 2),
        "distance_miles": float(t["trip_distance"]),
        "total_amount": float(t["total_amount"])
    }

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO NO HACER: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog, passenger_count):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1

    start = get_time()

    # Acumuladores
    total = 0
    durations_sum = 0.0
    cost_sum = 0.0
    distance_sum = 0.0
    tolls_sum = 0.0
    tips_sum = 0.0
    payment_counter = {}
    date_counter = {}

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Solo procesamos si cumple el filtro de pasajeros
        if int(trip["passenger_count"]) == passenger_count:
            total += 1

            # Duración
            durations_sum += trip_duration_minutes(trip)

            # Costos y distancias
            cost_sum += float(trip["total_amount"])
            distance_sum += float(trip["trip_distance"])
            tolls_sum += float(trip["tolls_amount"])
            tips_sum += float(trip["tip_amount"])

            # Medio de pago
            ptype = trip["payment_type"]
            payment_counter[ptype] = payment_counter.get(ptype, 0) + 1

            # Fecha (sin horas)
            date = trip["pickup_datetime"].split(" ")[0]
            date_counter[date] = date_counter.get(date, 0) + 1

    # Resultados
    if total > 0:
        avg_duration = durations_sum / total
        avg_cost = cost_sum / total
        avg_distance = distance_sum / total
        avg_tolls = tolls_sum / total
        avg_tips = tips_sum / total
        most_used_payment = max(payment_counter.items(), key=lambda x: x[1])
        most_used_date = max(date_counter.items(), key=lambda x: x[1])
    else:
        avg_duration = avg_cost = avg_distance = avg_tolls = avg_tips = 0.0
        most_used_payment = ("N/A", 0)
        most_used_date = ("N/A", 0)

    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total_filtered": total,
        "avg_duration_min": avg_duration,
        "avg_cost_usd": avg_cost,
        "avg_distance_miles": avg_distance,
        "avg_tolls_usd": avg_tolls,
        "avg_tips_usd": avg_tips,
        "most_used_payment": f"{most_used_payment[0]} - {most_used_payment[1]}",
        "most_frequent_date": most_used_date[0]
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
