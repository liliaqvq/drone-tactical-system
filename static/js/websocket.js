const socket = new WebSocket("ws://127.0.0.1:8765");

socket.onopen = () => {
    const status = document.getElementById("connection-status");
    status.innerText = "RADAR ONLINE";
    status.className = "px-3 py-1 bg-green-950 text-green-400 border border-green-700 rounded text-xs font-bold";
};

socket.onmessage = (event) => {
    const swarm = JSON.parse(event.data);
    
    // Actualiza marcadores del mapa
    updateMapMarkers(swarm);

    // Actualiza la barra lateral
    const droneListContainer = document.getElementById("drone-list");
    droneListContainer.innerHTML = "";
    let hasCriticalThreat = false;

    swarm.forEach(drone => {
        const isCritical = drone.threat_level === "CRITICAL";
        if (isCritical) hasCriticalThreat = true;

        const card = document.createElement("div");
        card.className = `p-2 border rounded ${isCritical ? 'bg-red-950/40 border-red-700' : 'bg-gray-950 border-gray-800'}`;
        card.innerHTML = `
            <div class="flex justify-between font-bold">
                <span class="text-white">${drone.drone_id}</span>
                <span class="${isCritical ? 'text-red-400 animate-pulse' : 'text-yellow-400'}">${drone.classification}</span>
            </div>
            <div class="text-[10px] text-gray-400 mt-1">
                Velocidad: ${drone.speed_kmh} km/h <br>
                Pos: ${drone.coordinates.lat}, ${drone.coordinates.lng}
            </div>
        `;
        droneListContainer.appendChild(card);
    });

    const alertBox = document.getElementById("alert-box");
    const threatText = document.getElementById("threat-level");
    
    if (hasCriticalThreat) {
        alertBox.className = "mt-6 p-3 bg-red-950 border border-red-600 text-center rounded animate-pulse";
        threatText.innerText = "¡INTRUSIÓN EN PERÍMETRO!";
        threatText.className = "text-sm font-bold text-red-500";
    } else {
        alertBox.className = "mt-6 p-3 bg-gray-950 border border-gray-800 text-center rounded";
        threatText.innerText = "SECTOR SEGURO";
        threatText.className = "text-sm font-bold text-green-400";
    }
};

socket.onclose = () => {
    const status = document.getElementById("connection-status");
    status.innerText = "RADAR OFFLINE";
    status.className = "px-3 py-1 bg-red-950 text-red-400 border border-red-700 rounded text-xs font-bold";
};