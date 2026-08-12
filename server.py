import asyncio
import json
import time
import websockets
from config import HOST, PORT
from models.drone import Drone
from services.geofence import GeofenceService

# Instanciación de objetos de la flota
fleet = [
    Drone("ALPHA-01", 37.7720, -122.4220, 82.5),
    Drone("BRAVO-02", 37.7710, -122.4150, 95.0),
    Drone("CHARLIE-03", 37.7700, -122.4180, 68.0)
]

async def send_swarm_telemetry(websocket):
    print("🟢 Cliente/Dashboard conectado al radar de enjambre!")
    try:
        while True:
            swarm_data = []
            current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ")

            for drone in fleet:
                drone.update_position()
                
                # Evaluación de perímetro usando el servicio dedicado
                in_restricted_zone = GeofenceService.is_inside_restricted_zone(drone.lat, drone.lng)
                
                classification = "FPV_HOSTILE" if in_restricted_zone else "UNIDENTIFIED"
                threat_level = "CRITICAL" if in_restricted_zone else "LOW"

                swarm_data.append(drone.to_dict(classification, threat_level, current_time))

            await websocket.send(json.dumps(swarm_data))
            print(f"📡 Transmitiendo datos de {len(swarm_data)} objetos...")
            await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosed:
        print("🔴 Cliente desconectado.")

async def main():
    async with websockets.serve(send_swarm_telemetry, HOST, PORT):
        print(f"📡 Servidor C-UAS corriendo en ws://{HOST}:{PORT}...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())