// Inicializa el mapa centrado
const map = L.map('map').setView([37.7750, -122.4194], 14);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Dibuja la Zona Restringida
const geofenceCircle = L.circle([37.7780, -122.4194], {
    color: '#ef4444',
    fillColor: '#f87171',
    fillOpacity: 0.25,
    radius: 500
}).addTo(map);

geofenceCircle.bindPopup("<b>ZONA RESTRINGIDA DE DEFENSA</b>");

const droneMarkers = {};

function updateMapMarkers(swarm) {
    swarm.forEach(drone => {
        const isCritical = drone.threat_level === "CRITICAL";
        const latLng = [drone.coordinates.lat, drone.coordinates.lng];

        if (!droneMarkers[drone.drone_id]) {
            droneMarkers[drone.drone_id] = L.circleMarker(latLng, {
                color: isCritical ? '#ef4444' : '#f59e0b',
                fillColor: isCritical ? '#dc2626' : '#d97706',
                fillOpacity: 0.9,
                radius: 8
            }).addTo(map).bindTooltip(drone.drone_id, { permanent: true, direction: 'right' });
        } else {
            droneMarkers[drone.drone_id].setLatLng(latLng);
            droneMarkers[drone.drone_id].setStyle({
                color: isCritical ? '#ef4444' : '#f59e0b',
                fillColor: isCritical ? '#dc2626' : '#d97706'
            });
        }
    });
}