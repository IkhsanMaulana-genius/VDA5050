import React from 'react';
import AGVInterface from './AGVInterface';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>VDA5050 AGV Simulator</h1>
        <p className="subtitle">MQTT Protocol Visualization Interface</p>
      </header>
      
      <main className="main-content">
        <div className="agv-container">
          <AGVInterface />
        </div>
        
        <div className="info-box">
          <h2>How to Use:</h2>
          <ol>
            <li>Click "Send Test Order" to start movement</li>
            <li>Monitor real-time position updates</li>
            <li>Use MQTT Explorer to inspect messages</li>
            <li>Connect to ws://localhost:9001 for raw MQTT</li>
          </ol>
        </div>
      </main>
    </div>
  );
};

export default App;