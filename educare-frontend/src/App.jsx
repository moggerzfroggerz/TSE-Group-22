import React, { useState } from 'react';
import './App.css';
import InputUI from './components/InputUI';
import DisplayOutput from './components/DisplayOutput';

export default function App() {
  const [userRole, setUserRole] = useState(null); 
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [history, setHistory] = useState([]); 
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGuestLogin = (role) => {
    setUserRole(role);
    setIsLoggedIn(true);
  };

  const handleQuerySubmit = async (query, role) => {
    setLoading(true);
    if (role === 'doctor') {
      setHistory(prev => [query.substring(0, 30) + "...", ...prev].slice(0, 5));
    }
    
    setTimeout(() => {
      setData({ text: "Sample AI Response for: " + query });
      setLoading(false);
    }, 1500);
  };

  if (!isLoggedIn) {
    return (
      <div className="login-page">
        <div className="login-card">
          {/* CSS-GENERATED LOGO */}
          <div className="brand-logo-container">
            <div className="medical-logo">
              <div className="medical-cross"></div>
            </div>
            <h1>EduCareAI</h1>
            <p>AI-Powered Health Assistant</p>
          </div>
          
          <div className="disabled-login">
            <input type="email" placeholder="Email Address" disabled />
            <button className="btn-disabled">Login with Email</button>
          </div>

          <div className="separator"><span>OR LOGIN AS GUEST</span></div>

          <div className="guest-options">
            <button className="btn-guest doctor" onClick={() => handleGuestLogin('doctor')}>
              Login as Clinician
            </button>
            <button className="btn-guest patient" onClick={() => handleGuestLogin('patient')}>
              Login as Patient
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`app-wrapper ${userRole}-theme`}>
      {userRole === 'doctor' && (
        <aside className="sidebar">
          <div className="sidebar-header">
             <div className="medical-logo mini">
                <div className="medical-cross mini"></div>
             </div>
            <span>Clinical Pro</span>
          </div>
          
          <nav className="sidebar-nav">
            <small>MAIN MENU</small>
            <ul>
              <li className="active">Dashboard</li>
              <li>Patient Files</li>
            </ul>

            <small>RECENT QUERIES</small>
            <ul className="history-list">
              {history.length > 0 ? history.map((item, i) => (
                <li key={i} className="history-item">{item}</li>
              )) : <li className="history-empty">No recent history</li>}
            </ul>
          </nav>

          <button className="logout-btn" onClick={() => setIsLoggedIn(false)}>Sign Out</button>
        </aside>
      )}

      <main className="main-content">
        <header className="top-bar">
          <h2>{userRole === 'doctor' ? 'Clinical Analysis' : 'Patient Portal'}</h2>
          {userRole === 'patient' && <button className="logout-link" onClick={() => setIsLoggedIn(false)}>Logout</button>}
        </header>

        <div className="content-area">
          <InputUI onSubmit={handleQuerySubmit} isLoading={loading} userRole={userRole} />
          {data && <DisplayOutput result={data} />}
        </div>
      </main>
    </div>
  );
}