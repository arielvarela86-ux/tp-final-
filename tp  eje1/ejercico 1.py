import re


def limpiar_registro_sensor(registro_raw):
    
    
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()
    
    
    temp_raw = str(registro_raw.get("temperatura", "0"))
    match = re.search(r"[-+]?\d*\.\d+|\d+", temp_raw)
    temperatura = float(match.group()) if match else 0.0
    
    
    ubicacion = registro_raw.get("ubicacion")
    if not ubicacion or not str(ubicacion).strip():
        ubicacion = "Planta General (No especificada)"
    else:
        ubicacion = str(ubicacion).strip()
        
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }



def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    
    lista_sensores_alerta = []
    suma_temperaturas = 0.0
    total_sensores = len(lista_sensores_limpios)
    
    if total_sensores == 0:
        return [], 0.0

    for sensor in lista_sensores_limpios:
        temp = sensor.get("temperatura", 0.0)
        suma_temperaturas += temp
        
        
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor.get("sensor_id"))
            
    promedio_temperatura = suma_temperaturas / total_sensores
    
    return lista_sensores_alerta, promedio_temperatura



if __name__ == "__main__":
    
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 38.2 °C ", "ubicacion": ""},
        {"sensor_id": " SENSOR-003 ", "temperatura": "19.0C", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-004", "temperatura": "41.8 C", "ubicacion": "Calderas Principales"}
    ]

    print("=== PROCESAMIENTO Y LIMPIEZA DE DATOS CRUDOS ===")
    
    
    registros_limpios = [limpiar_registro_sensor(reg) for reg in registros_crudos]
    
    
    UMBRAL_ALERTA = 35.0
    
    
    sensores_alerta, promedio_global = generar_resumen_sensores(registros_limpios, UMBRAL_ALERTA)
    
    
    print("\n" + "="*45)
    print("      REPORTE CONSOLIDADO ECOTECH SOLUTIONS")
    print("="*45)
    print(f"  Temperatura Global Promedio : {promedio_global:.2f} °C")
    print(f"  Umbral de Alerta Configurado : {UMBRAL_ALERTA} °C")
    print(f" Dispositivos en Alerta        : {len(sensores_alerta)} ({', '.join(sensores_alerta) if sensores_alerta else 'Ninguno'})")
    
    print("\n--- DETALLE DE REGISTROS SANITIZADOS ---")
    for reg in registros_limpios:
        estado_alerta = " [ALERTA ACTIVA]" if reg["temperatura"] > UMBRAL_ALERTA else " [Estable]"
        print(f" • ID: {reg['sensor_id']:<12} | Temp: {reg['temperatura']:>5.1f} °C | Ubicación: {reg['ubicacion']}{estado_alerta}")
    print("="*45)