import json
import time
import paho.mqtt.client as mqtt
from typing import Dict, Any
from datetime import datetime

class AGVSimulator:
    def __init__(self, mqtt_broker: str = "mosquitto"):
        self.client = mqtt.Client()
        self.client.connect(mqtt_broker, 1883)
        self._setup_callbacks()
        
        self.state = {
            "headerId": 1,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "manufacturer": "SimAGV",
            "serialNumber": "SIM-001",
            "position": {"x": 0.0, "y": 0.0, "theta": 0.0, "mapId": "factory"},
            "velocity": {"x": 0.0, "y": 0.0, "theta": 0.0},
            "batteryState": {"batteryCharge": 100.0, "batteryVoltage": 48.0},
            "operatingMode": "AUTOMATIC",
            "currentActions": [],
            "errors": [],
            "nodeStates": [],
            "edgeStates": [],
            "safetyState": {"eStop": False, "fieldViolation": False}
        }
        
        self.client.loop_start()

    def _setup_callbacks(self):
        self.client.on_message = self._on_message
        self.client.subscribe("vda5050/order")
        self.client.subscribe("vda5050/instantActions")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            if msg.topic == "vda5050/order":
                self._process_order(payload)
            elif msg.topic == "vda5050/instantActions":
                self._process_instant_actions(payload)
        except json.JSONDecodeError:
            print("Invalid JSON received")

    def _process_order(self, order: Dict[str, Any]):
        print(f"Processing order: {order.get('orderId')}")
        self.state["currentActions"] = order.get("actions", [])
        self._update_position()

    def _process_instant_actions(self, actions: Dict[str, Any]):
        for action in actions.get("instantActions", []):
            if action.get("actionType") == "STOP":
                self.state["operatingMode"] = "STOPPED"
            elif action.get("actionType") == "RESUME":
                self.state["operatingMode"] = "AUTOMATIC"

    def _update_position(self):
        if self.state["operatingMode"] == "AUTOMATIC" and self.state["currentActions"]:
            self.state["position"]["x"] += 0.1
            self.state["batteryState"]["batteryCharge"] = max(
                0, self.state["batteryState"]["batteryCharge"] - 0.1
            )
            self.state["timestamp"] = datetime.utcnow().isoformat()

    def publish_state(self):
        self.client.publish("vda5050/state", json.dumps(self.state))