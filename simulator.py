import asyncio
import json
import random
import time
import websockets

# Definimos 3 drones con sus coordenadas y velocidades iniciales
drones = [
    {"id": "ALPHA-01", "lat": 37.7720, "lng": -122.4220, "speed": 82.5},
    {"id": "BRAVO-02", "lat": 37.7710, "lng": -122.4150, "speed": 95.0},
    {"id": "CHARLIE-03", "lat": 37.7700, "lng": -122.4180, "speed": 68.0}
]

# Centro y radio de la zona restringida (Geofence)
GEOFENCE_CENTER = {"lat": 37.7780, "lng": -122.4194}
GEOFENCE_RADIUS = 0.005 # ~500 metros

async def send_swarm_telemetry(websocket):
    print("🟢 Cliente/Dashboard conectado al radar de enjambre!")
    
    try:
        while True:
            swarm_data = []
            
            for drone in drones:
                # Cada dron avanza en su propia trayectoria
                drone["lat"] += random.uniform(0.0001, 0.0003)
                drone["lng"] += random.uniform(0.0001, 0.0003)
                drone["speed"] = round(random.uniform(70.0, 100.0), 1)
                
                # Cálculo de distancia simple al centro del Geofence
                dist_lat = abs(drone["lat"] - GEOFENCE_CENTER["lat"])
                dist_lng = abs(drone["lng"] - GEOFENCE_CENTER["lng"])
                in_restricted_zone = (dist_lat < GEOFENCE_RADIUS) and (dist_lng < GEOFENCE_RADIUS)
                
                swarm_data.append({
                    "drone_id": drone["id"],
                    "classification": "FPV_HOSTILE" if in_restricted_zone else "UNIDENTIFIED",
                    "coordinates": {
                        "lat": round(drone["lat"], 6),
                        "lng": round(drone["lng"], 6)
                    },
                    "speed_kmh": drone["speed"],
                    "threat_level": "CRITICAL" if in_restricted_zone else "LOW",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                })

            # Envía la lista con TODO el enjambre en un solo paquete JSON
            await websocket.send(json.dumps(swarm_data))
            print(f"📡 Transmitiendo datos de {len(swarm_data)} objetos detectados...")
            
            await asyncio.sleep(1) # Transmite cada segundo
            
    except websockets.exceptions.ConnectionClosed:
        print("🔴 Cliente desconectado.")

async def main():
    async with websockets.serve(send_swarm_telemetry, "127.0.0.1", 8765):
        print("📡 Servidor C-UAS (Enjambre) corriendo en ws://127.0.0.1:8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())