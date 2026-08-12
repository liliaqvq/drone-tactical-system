import random

class Drone:
    def __init__(self, drone_id: str, initial_lat: float, initial_lng: float, initial_speed: float):
        self.drone_id = drone_id
        self.lat = initial_lat
        self.lng = initial_lng
        self.speed = initial_speed

    def update_position(self):
        """Simula el avance del dron en el espacio aéreo."""
        self.lat += random.uniform(0.0001, 0.0003)
        self.lng += random.uniform(0.0001, 0.0003)
        self.speed = round(random.uniform(70.0, 100.0), 1)

    def to_dict(self, classification: str, threat_level: str, timestamp: str) -> dict:
        """Sintetiza el estado del dron en el formato JSON esperado."""
        return {
            "drone_id": self.drone_id,
            "classification": classification,
            "coordinates": {
                "lat": round(self.lat, 6),
                "lng": round(self.lng, 6)
            },
            "speed_kmh": self.speed,
            "threat_level": threat_level,
            "timestamp": timestamp
        }