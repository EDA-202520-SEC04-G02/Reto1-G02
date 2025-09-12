import time

# Imports necesarios
import csv # Para cargar los datos
from DataStructures.List import array_list as lt # Importo mi implementación de lista para guardar la información
csv.field_size_limit(2147483647) # Consejo de la guía
from datetime import datetime # Importamos datetime, porque es MUCHO MEJOR para manejar fechas que hacer todo a mano
import math
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
    
    # iniciar tiempo
    start = get_time()

    # Cargar trayectos
    with open(taxisfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f)
        for row in input_file:
            lt.add_last(catalog["trips"], row) # Agrego cada fila como un dict a la lista

    # Cargar barrios
    with open(neighfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f, delimiter=";") # Esta carga de datos tiene la peculiaridad que usa ; como separador
        for row in input_file:
            lt.add_last(catalog["neighborhoods"], row) # Agrego cada fila como un dict a la lista

    # Procesar min/max y preview, se hizo con funciones externas
    min_trip, max_trip = find_min_max_trip(catalog["trips"])
    
    # Formatear preview con tabulate
    preview = get_preview_trips(catalog["trips"], 5)

    # parar tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total_trips": lt.size(catalog["trips"]),
        "min_trip": min_trip,
        "max_trip": max_trip,
        "preview": preview
    }

# Funciones de ayuda

def trip_duration_minutes(trip): # Esta función nos ayuda a sacar la diferencia de fechas
    """
    Calcula la duración en minutos de un trayecto
    """
    fmt = "%Y-%m-%d %H:%M:%S" # Formato de las fechas en el csv
    if "pickup_datetime" in trip and "dropoff_datetime" in trip: # If para entrar a las fechas de un trip en específico
        pickup = datetime.strptime(trip["pickup_datetime"], fmt)
        dropoff = datetime.strptime(trip["dropoff_datetime"], fmt)
        return (dropoff - pickup).total_seconds() / 60 # Diferencia en minutos
    else:
        return 0.0 # Por si acaso?


def find_min_max_trip(trips):
    """
    Encuentra el trayecto de menor y mayor distancia (distancia > 0)
    """
    min_trip = None
    max_trip = None
    size = lt.size(trips)
    for i in range(size): # Iteramos sobre cada viaje
        t = lt.get_element(trips, i) # accedemos a la información del viaje
        dist = float(t["trip_distance"]) # sacamos la distancia
        if dist > 0: # Entramos a comparar solo si la distancia es mayor a 0
            if min_trip is None or dist < float(min_trip["trip_distance"]): # Este primer if me da la distancia mínima, y va guardando el que cumpla la desigualdad
                min_trip = t
            if max_trip is None or dist > float(max_trip["trip_distance"]): # Misma idea pero con la otra desigualdad, así se puede hacer O(n)
                max_trip = t
    return min_trip, max_trip # DEvolvemos ambos viajes


def get_preview_trips(trips, n=5): # Función para hacer el preview con tabulate
    """
    Retorna los primeros y últimos n trayectos con los campos requeridos
    """
    preview = []
    size = lt.size(trips)

    # Primeros n
    for i in range(min(n, size)):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t)) # Guardamos los primeros 5

    # Últimos n
    for i in range(max(size - n, 0), size):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t)) # Guardamos los últimos 5

    return preview

def format_trip(t): # Formato según requerimientos
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
    
def find_nearest_neighborhood(neigh_list, lat, lon):
    """
    Encuentra el barrio más cercano a un punto (lat, lon)
    usando la lista de centroides de barrios
    """
    size = lt.size(neigh_list)
    min_dist = float("inf")
    nearest = None
    for i in range(size):
        neigh = lt.get_element(neigh_list, i)
        # Convertir coma decimal -> punto para usar float
        nlat = float(neigh["latitude"].replace(",", "."))
        nlon = float(neigh["longitude"].replace(",", "."))
        name = neigh["neighborhood"]

        d = haversine(lat, lon, nlat, nlon)
        if d < min_dist:
            min_dist = d
            nearest = name
    return nearest
    
def haversine(lat1, lon1, lat2, lon2): # Esto es literal sacado de ChatGPT porque son calculos que no entiendo
    """
    Calcula la distancia haversine en kilómetros entre dos puntos
    """
    R = 6371  # radio de la Tierra en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

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
    # TODO DONE: Modificar el requerimiento 1

    # inicio tiempo
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

    size = lt.size(catalog["trips"]) # Iteramos sobre cada viaje
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i) # Accedemos a la información del viaje

        # Solo procesamos si cumple el filtro de pasajeros
        if int(trip["passenger_count"]) == passenger_count:
            total += 1

            # Duración
            durations_sum += trip_duration_minutes(trip) # Re usamos la función que ya teníamos para duración de minutos

            # Costos y distancias, sumamos a los contadores que definimos arriba
            cost_sum += float(trip["total_amount"])
            distance_sum += float(trip["trip_distance"])
            tolls_sum += float(trip["tolls_amount"])
            tips_sum += float(trip["tip_amount"])

            # Medio de pago, este contador es un poco diferente, usamos un dict para contar cada tipo de pago
            ptype = trip["payment_type"]
            payment_counter[ptype] = payment_counter.get(ptype, 0) + 1

            # Fecha (sin horas) Para la fecha más frecuente, usamos otro dict para contar cada fecha (Ojo solo separamos por YYYY-MM-DD)
            date = trip["pickup_datetime"].split(" ")[0]
            date_counter[date] = date_counter.get(date, 0) + 1

    # Resultados, con los contadores retornamos los promedios y los más frecuentes
    if total > 0:
        avg_duration = durations_sum / total
        avg_cost = cost_sum / total
        avg_distance = distance_sum / total
        avg_tolls = tolls_sum / total
        avg_tips = tips_sum / total
        
        # Para payment_counter
        most_used_payment = None
        max_count = -1 # Contador inicial trivial
        for payment, count in payment_counter.items(): # Iteramos por cada medio de pago
            if count > max_count: # Vamos guardando el metodo de pago con mayor count
                max_count = count
                most_used_payment = (payment, count)

        # Para date_counter, misma lógica que el payment_counter
        most_used_date = None
        max_count = -1
        for date, count in date_counter.items():
            if count > max_count:
                max_count = count
                most_used_date = (date, count)

    # end time
    end = get_time()
    delta = delta_time(start, end)

    # retornamos resultados para imprimir
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


def req_4(catalog, filtro, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO DONE: Modificar el requerimiento 4
    
    start = get_time()

    # Convertir strings de fecha a objetos datetime.date
    date_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
    date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    combos = {}
    total_trips = 0

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Filtrar por fecha de pickup
        pickup_date = datetime.strptime(trip["pickup_datetime"], "%Y-%m-%d %H:%M:%S").date()
        if not (date_ini <= pickup_date <= date_fin):
            continue

        total_trips += 1

        # Identificar barrios
        plat, plon = float(trip["pickup_latitude"]), float(trip["pickup_longitude"])
        dlat, dlon = float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])

        origen = find_nearest_neighborhood(catalog["neighborhoods"], plat, plon)
        destino = find_nearest_neighborhood(catalog["neighborhoods"], dlat, dlon)

        if origen == destino or origen is None or destino is None:
            continue

        key = (origen, destino)

        if key not in combos:
            combos[key] = {
                "cost_sum": 0.0,
                "dist_sum": 0.0,
                "dur_sum": 0.0,
                "count": 0
            }

        combos[key]["cost_sum"] += float(trip["total_amount"])
        combos[key]["dist_sum"] += float(trip["trip_distance"])
        combos[key]["dur_sum"] += trip_duration_minutes(trip)
        combos[key]["count"] += 1

    # Calcular promedios y elegir
    best_combo = None
    best_val = None
    for (origen, destino), data in combos.items():
        avg_cost = data["cost_sum"] / data["count"]
        avg_dist = data["dist_sum"] / data["count"]
        avg_dur = data["dur_sum"] / data["count"]

        record = {
            "origen": origen,
            "destino": destino,
            "avg_cost": avg_cost,
            "avg_dist": avg_dist,
            "avg_dur": avg_dur
        }

        if best_combo is None:
            best_combo = record
            best_val = avg_cost
        else:
            if filtro == "MAYOR" and avg_cost > best_val:
                best_combo = record
                best_val = avg_cost
            elif filtro == "MENOR" and avg_cost < best_val:
                best_combo = record
                best_val = avg_cost

    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "filtro": filtro,
        "total_trips": total_trips,
        "combo": best_combo
    }


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
    # TODO NO HACER: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO NO HACER: Modificar el requerimiento 7
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
