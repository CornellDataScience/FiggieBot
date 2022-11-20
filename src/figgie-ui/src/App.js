import './App.css';
import Login from './pages/login/Login';
import Game from './pages/game/Game';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import { BrowserRouter, Routes, Route } from "react-router-dom"

const client = new W3CWebSocket('ws://127.0.0.1:8000/ws');

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login client={client} />} />
          <Route path="/game" element={<Game client={client} />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
