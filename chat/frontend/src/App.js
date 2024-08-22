import React, { useState } from 'react';
import './App.css';
import { FaSun, FaMoon } from 'react-icons/fa'; // Importa ícones de dia/noite

function App() {
  const [pergunta, setPergunta] = useState('');
  const [resposta, setResposta] = useState('');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const enviarPergunta = async (e) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch('http://localhost:5000/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pergunta, usuario_id: 1 }),
    });
    const data = await response.json();
    setResposta(data.resposta);
    setLoading(false);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
        <div className="flower-side left"></div>
        <div className="flower-side right"></div>
        <div className="animated-object" style={{ top: '10%', left: '20%' }}></div>
        <div className="animated-object" style={{ top: '50%', left: '60%' }}></div>
        <div className="animated-object" style={{ top: '80%', left: '30%' }}></div>
        <div className="animated-object" style={{ top: '30%', left: '70%' }}></div>
      <button className="mode-toggle-button" onClick={toggleDarkMode}>
        {darkMode ? <FaSun /> : <FaMoon />} {/* Ícones de modo claro/escuro */}
      </button>
      <h1>Oráculo Dadaísta</h1>
      <form onSubmit={enviarPergunta} className="question-form">
        <input
          type="text"
          value={pergunta}
          onChange={(e) => setPergunta(e.target.value)}
          placeholder="Faça uma pergunta"
          className="question-input"
        />
        <button type="submit" className="submit-button">Enviar</button>
      </form>
      <div className="response-container">
        <h2>Resposta:</h2>
        {loading ? (
          <div className="loading-container">
            <div className="loading-text">Carregando...</div>
            <div className="loader"></div>
          </div>
        ) : (
          <p>{resposta}</p>
        )}
      </div>
    </div>
  );
}

export default App;
