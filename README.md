# 🛡️ C-UAS Multi-Target Telemetry & Command Center

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![WebSocket Protocol](https://img.shields.io/badge/WebSocket-WS-green?style=for-the-badge&logo=websocket&logoColor=white)
![JavaScript / Leaflet](https://img.shields.io/badge/Frontend-JS%20%2F%20Leaflet-yellow?style=for-the-badge&logo=javascript&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

A real-time Counter-Unmanned Aircraft Systems (C-UAS) tactical monitoring platform and telemetry engine. This application simulates swarm drone intrusions, processes live geospatial telemetry over WebSockets, and renders dynamic threat tracking and geofence alerts on a dark-mode command dashboard.

---

## 📸 System Preview

```text
+-----------------------------------------------------------------------------------+
| 🛡️ MULTI-TARGET C-UAS RADAR                             [ RADAR ONLINE ]          |
+--------------------------------------------------+--------------------------------+
|                                                  | DETECTED THREATS               |
|                                                  |                                |
|        (🔴 ALPHA-01)                             | [ ALPHA-01 ] - FPV_HOSTILE     |
|              \                                   | Lat: 37.7782 | Lng: -122.4190   |
|               \                                  | Speed: 88.4 km/h               |
|                v                                 |                                |
|          +------------+                          | [ BRAVO-02 ] - UNIDENTIFIED   |
|          |  GEOFENCE  |                          | Lat: 37.7731 | Lng: -122.4162   |
|          | (RESTRICTED|                          | Speed: 94.2 km/h               |
|          |    ZONE)   |                          |                                |
|          +------------+                          +--------------------------------+
|                   ^                              | PERIMETER STATUS               |
|                  /                               |                                |
|        (🟡 BRAVO-02)                             | 🚨 INTRUSION IN PERIMETER      |
+--------------------------------------------------+--------------------------------+
```

---

## 📑 Table of Contents
- [Architecture & Data Flow](#-architecture--data-flow)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [JSON Telemetry Schema](#-json-telemetry-schema)
- [Getting Started](#-getting-started)
- [QA Automation & Roadmap](#-qa-automation--roadmap)
- [License](#-license)

---

## 🏗️ Architecture & Data Flow

The system employs an event-driven architecture designed for low-latency telemetry streaming:

```
+--------------------------+                 +--------------------------+
|  Python Telemetry Engine |  WebSockets     |  Tactical Web Dashboard  |
|  (simulator.py)          |  (ws://127.0.0.1|  (index.html / Leaflet)  |
|                          |   :8765)        |                          |
|  * Asynchronous Loop     | --------------> |  * Map Rendering Engine  |
|  * Swarm Vector Calc     |  JSON Payloads  |  * Swarm Markers         |
|  * Geofence Evaluator    |                 |  * Real-Time UI Alerts   |
+--------------------------+                 +--------------------------+
```

1. **Backend Telemetry Engine (`simulator.py`)**: Continuously updates geospatial coordinates, velocities, and threat levels for active airborne targets in an asynchronous `asyncio` event loop.
2. **WebSocket Pipeline (`websockets`)**: Transmits full JSON swarm payloads at 1 Hz intervals over local network port `8765`.
3. **Command & Control UI (`index.html`)**: Consumes incoming streams, dynamically creates/updates vector markers on a Leaflet map, and evaluates global perimeter breach thresholds.

---

## ✨ Key Features

- 🛸 **Multi-Target Swarm Tracking**: Real-time position and trajectory rendering for multiple airborne targets simultaneously (`ALPHA-01`, `BRAVO-02`, `CHARLIE-03`).
- 🎯 **Automated Geofencing**: Evaluates perimeter breach status against a defined Defense Restricted Zone (~500m radius).
- 🚨 **Dynamic Threat Classification**: Automatically escalates threat levels from `LOW / UNIDENTIFIED` to `CRITICAL / FPV_HOSTILE` upon perimeter entry.
- 🗺️ **Tactical Dark-Mode UI**: Built with Tailwind CSS and CartoDB Dark Matter tile basemaps for high-contrast visibility.
- ⚡ **Low Latency**: Async WebSocket connection ensures real-time UI updates without HTTP polling overhead.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, `asyncio`, `websockets`, `json`
- **Frontend**: HTML5, JavaScript (ES6+), Tailwind CSS (CDN), Leaflet.js
- **Protocols**: WebSocket (`ws://`)
- **Dev Tools**: VS Code, Live Server

---

## 📁 Repository Structure

```text
drone-tactical-system/
│
├── simulator.py     # Python WebSocket server & multi-target telemetry engine
├── index.html       # Tactical command dashboard (Leaflet.js + Tailwind CSS)
└── README.md        # System documentation
```

---

## 📡 JSON Telemetry Schema

The backend broadcasts telemetry packages formatted according to standard C-UAS sensor formats:

```json
[
  {
    "drone_id": "ALPHA-01",
    "classification": "FPV_HOSTILE",
    "coordinates": {
      "lat": 37.778102,
      "lng": -122.419105
    },
    "speed_kmh": 88.45,
    "threat_level": "CRITICAL",
    "timestamp": "2026-08-12T14:45:00Z"
  },
  {
    "drone_id": "BRAVO-02",
    "classification": "UNIDENTIFIED",
    "coordinates": {
      "lat": 37.773110,
      "lng": -122.416200
    },
    "speed_kmh": 94.20,
    "threat_level": "LOW",
    "timestamp": "2026-08-12T14:45:00Z"
  }
]
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed on your system.
- **VS Code** (recommended) with the **Live Server** extension.

### Installation & Execution

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/your-username/c-uas-drone-tactical-system.git
   cd c-uas-drone-tactical-system
   ```

2. **Install Python dependencies**:
   ```bash
   pip install websockets
   ```

3. **Start the Telemetry Server**:
   ```bash
   python simulator.py
   ```
   *You should see:* `📡 Servidor C-UAS (Enjambre) corriendo en ws://127.0.0.1:8765...`

4. **Launch the Dashboard**:
   - Right-click `index.html` in VS Code and select **"Open with Live Server"**.
   - Alternatively, serve `index.html` through any local HTTP server (e.g., `python -m http.server 5500`).

---

## 🧪 QA Automation & Future Roadmap

- [ ] **Playwright Test Suite**: Implement automated end-to-end tests validating WebSocket connection state, target card rendering, and UI alert escalation.
- [ ] **Electron Packaging**: Wrap the frontend into a standalone Desktop application for offline deployment.
- [ ] **Bidirectional Mitigation**: Add an interactive "EMP Intercept" button on the UI to send neutralization commands back to the Python backend.
- [ ] **OpenCV / Hardware Integration**: Connect real RTSP video streams and YOLO object detection models for physical drone recognition.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
