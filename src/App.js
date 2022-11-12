import './App.css';
import Login from './pages/login/Login';
import Game from './pages/game/Game';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8000/ws');

function App() {
  return (
    <div className="App">
      {/* < Login /> */}
      < Game client={client} />
    </div>
  );
}

export default App;
