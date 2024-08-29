import React, { useState } from 'react';
import './App.css';
import { FaSun, FaMoon } from 'react-icons/fa';

const ModeToggleButton = ({ darkMode, toggleDarkMode }) => (
  <button className="mode-toggle-button" onClick={toggleDarkMode}>
    {darkMode ? <FaSun /> : <FaMoon />}
  </button>
);

const QuestionForm = ({ pergunta, setPergunta, enviarPergunta, enabled }) => (
  <form onSubmit={enviarPergunta} className="question-form">
    <input
      type="text"
      value={pergunta}
      onChange={(e) => setPergunta(e.target.value)}
      placeholder="Faça uma pergunta"
      className="question-input"
      disabled={!enabled}
    />
    <button type="submit" className="submit-button" disabled={!enabled}>
      Enviar
    </button>
  </form>
);

const ResponseContainer = ({ loading, resposta }) => (
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
);

function App() {
  const [pergunta, setPergunta] = useState('');
  const [resposta, setResposta] = useState('');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const enviarPergunta = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pergunta }),
      });
      const data = await response.json();
      if (response.ok) {
        setResposta(data.resposta);
      } else {
        setResposta(data.erro || 'Erro ao obter resposta. Tente novamente.');
      }
    } catch (error) {
      setResposta('Erro ao obter resposta. Tente novamente.');
    }
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
      
      <ModeToggleButton darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <h1>Oráculo Dadaísta</h1>
      
      <QuestionForm pergunta={pergunta} setPergunta={setPergunta} enviarPergunta={enviarPergunta} enabled={!loading} />
      
      <ResponseContainer loading={loading} resposta={resposta} />
    </div>
  );
}

export default App;
