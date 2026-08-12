from config import GEOFENCE_CENTER, GEOFENCE_RADIUS

class GeofenceService:
    @staticmethod
    def is_inside_restricted_zone(lat: float, lng: float) -> bool:
        """Calcula si la coordenada está dentro del radio de exclusión."""
        dist_lat = abs(lat - GEOFENCE_CENTER["lat"])
        dist_lng = abs(lng - GEOFENCE_CENTER["lng"])
        return (dist_lat < GEOFENCE_RADIUS) and (dist_lng < GEOFENCE_RADIUS)