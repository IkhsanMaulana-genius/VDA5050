import React, { useState, useEffect } from 'react';
import mqtt, { MqttClient } from 'mqtt';

interface AGVState {
  position: { x: number; y: number; theta: number };
  batteryState: { batteryCharge: number };
  operatingMode: string;
  timestamp: string;
}

const AGVInterface: React.FC = () => {
  const [agvState, setAgvState] = useState<AGVState | null>(null);
  const [client, setClient] = useState<MqttClient | null>(null);

  useEffect(() => {
    const mqttClient = mqtt.connect('ws://localhost:9001');
    setClient(mqttClient);

    mqttClient.subscribe('vda5050/state');
    mqttClient.on('message', (topic, payload) => {
      if (topic === 'vda5050/state') {
        setAgvState(JSON.parse(payload.toString()));
      }
    });

    return () => {
      mqttClient.end();
    };
  }, []);

  const sendTestOrder = () => {
    const order = {
      headerId: 1,
      orderId: `ORDER_${Date.now()}`,
      nodes: [
        {
          nodeId: "N1",
          sequenceId: 0,
          nodePosition: { x: 10, y: 5, theta: 0, mapId: "factory" }
        }
      ]
    };
    client?.publish('vda5050/order', JSON.stringify(order));
  };

  return (
    <div>
      <h1>AGV Simulator Interface</h1>
      {agvState && (
        <div>
          <h2>Position</h2>
          <p>X: {agvState.position.x.toFixed(2)}</p>
          <p>Y: {agvState.position.y.toFixed(2)}</p>
          
          <h2>Battery</h2>
          <p>{agvState.batteryState.batteryCharge.toFixed(1)}%</p>
          
          <h2>Status</h2>
          <p>Mode: {agvState.operatingMode}</p>
          <p>Last Update: {new Date(agvState.timestamp).toLocaleTimeString()}</p>
        </div>
      )}
      
      <button onClick={sendTestOrder}>Send Test Order</button>
    </div>
  );
};

export default AGVInterface;