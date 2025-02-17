import json
import time
import paho.mqtt.client as mqtt

class AGVSimulator:
    def __init__(self):
        self.client = mqtt.Client()
        self.state = {
            "position": {"x": 0, "y": 0},
            "battery": 100.0,
            "currentOrder": None,
            "errors": []
        }
        
        # Connect to MQTT
        self.client.connect("mqtt", 1883)  # "mqtt" = Docker service name
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
        
        # Publish initial factsheet
        self.publish_factsheet()
        
        # Start state updates
        while True:
            self.publish_state()
            time.sleep(2)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker")
        self.client.subscribe("vda5050/order")
        self.client.subscribe("vda5050/instantActions")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        
        if topic == "vda5050/order":
            print(f"Received order: {payload}")
            self.process_order(payload)
        elif topic == "vda5050/instantActions":
            print(f"Received action: {payload}")

    def process_order(self, order):
        self.state["currentOrder"] = order
        for node in order["nodes"]:
            self.state["position"] = {"x": node["x"], "y": node["y"]}
            self.publish_state()
            time.sleep(1)  # Simulate movement

    def publish_state(self):
        self.client.publish("vda5050/state", json.dumps(self.state))

    def publish_factsheet(self):
        factsheet = {
            "agvId": "sim_agv_01",
            "type": "Simulated AGV",
            "maxBattery": 100.0,
            "loadCapacity": 50.0
        }
        self.client.publish("vda5050/factsheet", json.dumps(factsheet))

if __name__ == "__main__":
    AGVSimulator()