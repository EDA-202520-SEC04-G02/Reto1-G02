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
    # TODO DONE: Realizar la carga de datos
    
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
    Encuentra el barrio más cercano a un punto (lat, lon) usando la lista de centroides de barrios
    """
    size = lt.size(neigh_list)
    nearest_name = None
    min_dist = None  # empezamos sin valor

    for i in range(size):
        neigh = lt.get_element(neigh_list, i)
        nlat = float(neigh["latitude"].replace(",", ".")) # NO MÁS COMAS, ARRIBA LOS PUNTOS!
        nlon = float(neigh["longitude"].replace(",", "."))
        dist = haversine(lat, lon, nlat, nlon) # Uso la función recomendada para sacar la distancia entre los puntos

        if min_dist is None or dist < min_dist:
            min_dist = dist
            nearest_name = neigh["neighborhood"]

    return nearest_name
    
def haversine(lat1, lon1, lat2, lon2): # Esto es literal sacado de ChatGPT porque son calculos y ya
    """
    Calcula la distancia haversine en kilómetros entre dos puntos
    """
    R = 3959  # radio de la Tierra en mi
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


def req_2(catalog, payment_method):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO DONE: Modificar el requerimiento 2

    # inicio tiempo
    start = get_time()

    # Acumuladores
    total = 0
    durations_sum = 0.0
    cost_sum = 0.0
    distance_sum = 0.0
    tolls_sum = 0.0
    tips_sum = 0.0
    passenger_counter = {}
    date_counter = {}

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Solo procesamos si cumple el filtro del método de pago
        if trip["payment_type"] == payment_method:
            total += 1

            # Duración
            durations_sum += trip_duration_minutes(trip)

            # Costos y distancias
            cost_sum += float(trip["total_amount"])
            distance_sum += float(trip["trip_distance"])
            tolls_sum += float(trip["tolls_amount"])
            tips_sum += float(trip["tip_amount"])

            # Contador de número de pasajeros
            pcount = trip["passenger_count"]
            passenger_counter[pcount] = passenger_counter.get(pcount, 0) + 1

            # Fecha de finalización más frecuente
            date = trip["dropoff_datetime"].split(" ")[0]
            date_counter[date] = date_counter.get(date, 0) + 1

    # Resultados
    if total > 0:
        avg_duration = durations_sum / total
        avg_cost = cost_sum / total
        avg_distance = distance_sum / total
        avg_tolls = tolls_sum / total
        avg_tips = tips_sum / total

        # Pasajeros más frecuentes
        most_used_passenger = None
        max_count = -1
        for pcount, count in passenger_counter.items():
            if count > max_count:
                max_count = count
                most_used_passenger = (pcount, count)

        # Fecha más frecuente
        most_used_date = None
        max_count = -1
        for date, count in date_counter.items():
            if count > max_count:
                max_count = count
                most_used_date = (date, count)
    else: # 
        avg_duration = avg_cost = avg_distance = avg_tolls = avg_tips = 0
        most_used_passenger = None
        most_used_date = None

    # fin tiempo
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
        "most_used_passenger": f"{most_used_passenger[0]} - {most_used_passenger[1]}" if most_used_passenger else None,
        "most_frequent_date": most_used_date[0] if most_used_date else None
    }

def req_3(catalog, min_cost, max_cost):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO DONE: Modificar el requerimiento 3
    
    # inicio tiempo
    start = get_time()

    # Acumuladores
    total = 0
    durations_sum = 0.0
    cost_sum = 0.0
    distance_sum = 0.0
    tolls_sum = 0.0
    tips_sum = 0.0
    passenger_counter = {}
    date_counter = {}

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        amount = float(trip["total_amount"])
        if min_cost <= amount <= max_cost:
            total += 1

            # Duración
            durations_sum += trip_duration_minutes(trip)

            # Costos y distancias
            cost_sum += amount
            distance_sum += float(trip["trip_distance"])
            tolls_sum += float(trip["tolls_amount"])
            tips_sum += float(trip["tip_amount"])

            # Contador de número de pasajeros
            pcount = trip["passenger_count"]
            passenger_counter[pcount] = passenger_counter.get(pcount, 0) + 1

            # Fecha de finalización más frecuente
            date = trip["dropoff_datetime"].split(" ")[0]
            date_counter[date] = date_counter.get(date, 0) + 1

    # Resultados
    if total > 0:
        avg_duration = durations_sum / total
        avg_cost = cost_sum / total
        avg_distance = distance_sum / total
        avg_tolls = tolls_sum / total
        avg_tips = tips_sum / total

        # Pasajeros más frecuentes
        most_used_passenger = None
        max_count = -1
        for pcount, count in passenger_counter.items():
            if count > max_count:
                max_count = count
                most_used_passenger = (pcount, count)

        # Fecha más frecuente
        most_used_date = None
        max_count = -1
        for date, count in date_counter.items():
            if count > max_count:
                max_count = count
                most_used_date = (date, count)
    else:
        avg_duration = avg_cost = avg_distance = avg_tolls = avg_tips = 0
        most_used_passenger = None
        most_used_date = None

    # fin tiempo
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
        "most_used_passenger": f"{most_used_passenger[0]} - {most_used_passenger[1]}" if most_used_passenger else None,
        "most_frequent_date": most_used_date[0] if most_used_date else None
    }



def req_4(catalog, filtro, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO DONE: Modificar el requerimiento 4
    
        # inicio tiempo
    start = get_time()

    # Convertimos strings a fechas
    date_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
    date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    combos = {}  # Diccionario de combinaciones origen-destino
    total_trips = 0

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Fecha del pickup
        pickup_date = datetime.strptime(trip["pickup_datetime"], "%Y-%m-%d %H:%M:%S").date()

        # Solo procesamos si está dentro del rango
        if date_ini <= pickup_date <= date_fin:
            total_trips += 1

            # Identificar barrios
            plat, plon = float(trip["pickup_latitude"]), float(trip["pickup_longitude"])
            dlat, dlon = float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])
            
            # Aquí usamos esta función para determinar el más cercano según centroide
            
            origen = find_nearest_neighborhood(catalog["neighborhoods"], plat, plon)
            destino = find_nearest_neighborhood(catalog["neighborhoods"], dlat, dlon)

            # Solo consideramos si origen y destino son diferentes y válidos
            if origen is not None and destino is not None and origen != destino:

                key = (origen, destino)

                if key not in combos:
                    combos[key] = {
                        "cost_sum": 0.0,
                        "dist_csv_sum": 0.0,   # distancia del CSV
                        "dist_hav_sum": 0.0,   # distancia con haversine
                        "dur_sum": 0.0,
                        "count": 0
                    }
                # El contador es un poco más comlicado, porque armamos el key con una tupla, para poder comparar despues
                # Sumamos costo, distancia reportada en el CSV y duración
                combos[key]["cost_sum"] += float(trip["total_amount"])
                combos[key]["dist_csv_sum"] += float(trip["trip_distance"])
                combos[key]["dist_hav_sum"] += haversine(plat, plon, dlat, dlon)
                combos[key]["dur_sum"] += trip_duration_minutes(trip)
                combos[key]["count"] += 1


    # Elegir combinación según filtro
    best_combo = None
    best_val = None

    for (origen, destino), data in combos.items(): # Iteramos en cada combo de barrios
        
        # Para cada uno calculamos los avg
        avg_cost = data["cost_sum"] / data["count"]
        avg_dist_csv = data["dist_csv_sum"] / data["count"]
        avg_dist_hav = data["dist_hav_sum"] / data["count"]
        avg_dur = data["dur_sum"] / data["count"]


        # Cuardamos estos datos para comparar
        record = {
            "origen": origen,
            "destino": destino,
            "avg_cost": avg_cost,
            "avg_dist_csv": avg_dist_csv,
            "avg_dist_hav": avg_dist_hav,
            "avg_dur": avg_dur
        }

        # Comparamos dependiendo el filtro y así encontramos el mejor o peor combo
        if best_combo is None:
            best_combo = record
            best_val = avg_cost
        elif filtro == "MAYOR" and avg_cost > best_val:
            best_combo = record
            best_val = avg_cost
        elif filtro == "MENOR" and avg_cost < best_val:
            best_combo = record
            best_val = avg_cost

    # fin tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "filtro": filtro,
        "total_trips": total_trips,
        "combo": best_combo
    }

def req_5(catalog, filtro, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO DONE: Modificar el requerimiento 5

    # inicio tiempo
    start = get_time()

    # Convertir strings de fecha a objetos datetime.date
    date_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
    date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    franjas = {}   # Diccionario {franja: {..}}
    total_trips = 0

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i) # entramos al catalogo como siempre lo hemos hecho

        # Fecha de pickup
        pickup_dt = datetime.strptime(trip["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
        pickup_date = pickup_dt.date()

        # Filtrar por rango de fechas
        if date_ini <= pickup_date <= date_fin: 
            total_trips += 1

            # Definir franja [h - h+1)
            hour = pickup_dt.hour
            franja = f"[{hour:02d} - {hour+1:02d})" # Formato de la franja segun la guía

            # Si no existe la franja, inicializar
            if franja not in franjas:
                franjas[franja] = {
                    "cost_sum": 0.0,
                    "dur_sum": 0.0,
                    "pass_sum": 0,
                    "count": 0,
                    "max_trip": None,
                    "min_trip": None
                }

            # Cuadramos datos
            cost = float(trip["total_amount"])
            duration = trip_duration_minutes(trip)
            passengers = int(trip["passenger_count"])

            # Acumulamos los datos
            franjas[franja]["cost_sum"] += cost
            franjas[franja]["dur_sum"] += duration
            franjas[franja]["pass_sum"] += passengers
            franjas[franja]["count"] += 1

            # Actualizar viaje más caro (desempate por dropoff más reciente)
            if franjas[franja]["max_trip"] is None:
                franjas[franja]["max_trip"] = trip
            else:
                max_trip = franjas[franja]["max_trip"]
                if cost > float(max_trip["total_amount"]):
                    franjas[franja]["max_trip"] = trip
                elif cost == float(max_trip["total_amount"]):
                    if trip["dropoff_datetime"] > max_trip["dropoff_datetime"]:
                        franjas[franja]["max_trip"] = trip

            # Actualizar viaje más barato (desempate por dropoff más reciente)
            if franjas[franja]["min_trip"] is None:
                franjas[franja]["min_trip"] = trip
            else:
                min_trip = franjas[franja]["min_trip"]
                if cost < float(min_trip["total_amount"]):
                    franjas[franja]["min_trip"] = trip
                elif cost == float(min_trip["total_amount"]):
                    if trip["dropoff_datetime"] > min_trip["dropoff_datetime"]:
                        franjas[franja]["min_trip"] = trip

    # Elegir franja según filtro
    best_franja = None
    best_val = None

    for franja, data in franjas.items():
        avg_cost = data["cost_sum"] / data["count"]
        avg_dur = data["dur_sum"] / data["count"]
        avg_pass = data["pass_sum"] / data["count"]

        record = {
            "franja": franja,
            "avg_cost": avg_cost,
            "count": data["count"],
            "avg_dur": avg_dur,
            "avg_pass": avg_pass,
            "max_cost": float(data["max_trip"]["total_amount"]),
            "min_cost": float(data["min_trip"]["total_amount"])
        }

        if best_franja is None:
            best_franja = record
            best_val = avg_cost
        elif filtro == "MAYOR" and avg_cost > best_val:
            best_franja = record
            best_val = avg_cost
        elif filtro == "MENOR" and avg_cost < best_val:
            best_franja = record
            best_val = avg_cost

    # fin tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "filtro": filtro,
        "total_trips": total_trips,
        "franja": best_franja
    }


def req_6(catalog, barrio_inicio, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO DONE : Modificar el requerimiento 6

    # inicio tiempo
    start = get_time()

    # Convertir strings de fecha a objetos datetime.date
    date_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
    date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    total_trips = 0
    dist_sum = 0.0
    dur_sum = 0.0
    dest_counter = {}   # Contador de barrios destino
    pay_stats = {}      # Estadísticas por método de pago

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Fecha de pickup
        pickup_dt = datetime.strptime(trip["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
        pickup_date = pickup_dt.date()

        # Filtrar por rango de fechas
        if date_ini <= pickup_date <= date_fin:

            # Identificar barrio de origen con haversine
            plat, plon = float(trip["pickup_latitude"]), float(trip["pickup_longitude"])
            origen = find_nearest_neighborhood(catalog["neighborhoods"], plat, plon)

            # Solo procesamos si coincide con el barrio buscado
            if origen == barrio_inicio:
                total_trips += 1

                # Identificar barrio de destino
                dlat, dlon = float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])
                destino = find_nearest_neighborhood(catalog["neighborhoods"], dlat, dlon)

                # Acumuladores generales
                dist_sum += float(trip["trip_distance"])
                dur_sum += trip_duration_minutes(trip)

                # Contador de destinos
                if destino not in dest_counter:
                    dest_counter[destino] = 0
                dest_counter[destino] += 1

                # Estadísticas por medio de pago
                ptype = trip["payment_type"]
                if ptype not in pay_stats:
                    pay_stats[ptype] = {
                        "count": 0,
                        "cost_sum": 0.0,
                        "dur_sum": 0.0
                    }
                pay_stats[ptype]["count"] += 1
                pay_stats[ptype]["cost_sum"] += float(trip["total_amount"])
                pay_stats[ptype]["dur_sum"] += trip_duration_minutes(trip)

    # Si no hubo viajes, retornamos vacío
    if total_trips == 0:
        end = get_time()
        delta = delta_time(start, end)
        return {
            "time_ms": delta,
            "total_trips": 0,
            "avg_dist": 0,
            "avg_dur": 0,
            "most_visited": None,
            "payments": []
        }

    # Promedios generales
    avg_dist = dist_sum / total_trips
    avg_dur = dur_sum / total_trips

    # Barrio destino más frecuente
    most_visited = None
    max_dest_count = -1
    for dest, count in dest_counter.items():
        if count > max_dest_count:
            most_visited = dest
            max_dest_count = count

    # Estadísticas por método de pago
    max_used = None
    max_used_count = -1
    max_revenue = None
    max_revenue_val = -1.0

    for ptype, stats in pay_stats.items():
        if stats["count"] > max_used_count:
            max_used = ptype
            max_used_count = stats["count"]
        if stats["cost_sum"] > max_revenue_val:
            max_revenue = ptype
            max_revenue_val = stats["cost_sum"]

    payments_result = []
    for ptype, stats in pay_stats.items():
        record = {
            "payment": ptype,
            "count": stats["count"],
            "avg_cost": stats["cost_sum"] / stats["count"],
            "avg_dur": stats["dur_sum"] / stats["count"],
            "is_most_used": (ptype == max_used),
            "is_max_revenue": (ptype == max_revenue)
        }
        payments_result.append(record)

    # fin tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total_trips": total_trips,
        "avg_dist": avg_dist,
        "avg_dur": avg_dur,
        "most_visited": most_visited,
        "payments": payments_result
    }



def req_7(catalog, barrio_inicio, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO BONUS: Modificar el requerimiento 7
    """
    Requerimiento 7:
    Igual que el Req 6, pero excluyendo trayectos cuyo destino sea el mismo barrio de origen.
    """

    # inicio tiempo
    start = get_time()

    # Convertir strings de fecha a objetos datetime.date
    date_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
    date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    total_trips = 0
    dist_sum = 0.0
    dur_sum = 0.0
    dest_counter = {}
    pay_stats = {}

    size = lt.size(catalog["trips"])
    for i in range(size):
        trip = lt.get_element(catalog["trips"], i)

        # Fecha de pickup
        pickup_dt = datetime.strptime(trip["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
        pickup_date = pickup_dt.date()

        if date_ini <= pickup_date <= date_fin:
            # Identificar barrio origen
            plat, plon = float(trip["pickup_latitude"]), float(trip["pickup_longitude"])
            origen = find_nearest_neighborhood(catalog["neighborhoods"], plat, plon)

            if origen == barrio_inicio:
                # Identificar destino
                dlat, dlon = float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])
                destino = find_nearest_neighborhood(catalog["neighborhoods"], dlat, dlon)

                # EXCLUIR viajes donde origen == destino
                if destino != origen:
                    total_trips += 1

                    # Acumuladores generales
                    dist_sum += float(trip["trip_distance"])
                    dur_sum += trip_duration_minutes(trip)

                    # Contador de destinos
                    if destino not in dest_counter:
                        dest_counter[destino] = 0
                    dest_counter[destino] += 1

                    # Estadísticas de pago
                    ptype = trip["payment_type"]
                    if ptype not in pay_stats:
                        pay_stats[ptype] = {
                            "count": 0,
                            "cost_sum": 0.0,
                            "dur_sum": 0.0
                        }
                    pay_stats[ptype]["count"] += 1
                    pay_stats[ptype]["cost_sum"] += float(trip["total_amount"])
                    pay_stats[ptype]["dur_sum"] += trip_duration_minutes(trip)

    # Si no hubo viajes, devolvemos vacío
    if total_trips == 0:
        end = get_time()
        delta = delta_time(start, end)
        return {
            "time_ms": delta,
            "total_trips": 0,
            "avg_dist": 0,
            "avg_dur": 0,
            "most_visited": None,
            "payments": []
        }

    # Promedios generales
    avg_dist = dist_sum / total_trips
    avg_dur = dur_sum / total_trips

    # Barrio destino más frecuente (distinto al origen)
    most_visited = None
    max_count = -1
    for dest, count in dest_counter.items():
        if count > max_count:
            most_visited = dest
            max_count = count

    # Pago más usado y el que más recaudó
    max_used = None
    max_used_count = -1
    max_revenue = None
    max_revenue_val = -1.0

    for ptype, stats in pay_stats.items():
        if stats["count"] > max_used_count:
            max_used = ptype
            max_used_count = stats["count"]
        if stats["cost_sum"] > max_revenue_val:
            max_revenue = ptype
            max_revenue_val = stats["cost_sum"]

    payments_result = []
    for ptype, stats in pay_stats.items():
        record = {
            "payment": ptype,
            "count": stats["count"],
            "avg_cost": stats["cost_sum"] / stats["count"],
            "avg_dur": stats["dur_sum"] / stats["count"],
            "is_most_used": (ptype == max_used),
            "is_max_revenue": (ptype == max_revenue)
        }
        payments_result.append(record)

    # fin tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total_trips": total_trips,
        "avg_dist": avg_dist,
        "avg_dur": avg_dur,
        "most_visited": most_visited,
        "payments": payments_result
    }



def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO NO HACER: Modificar el requerimiento 8
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
