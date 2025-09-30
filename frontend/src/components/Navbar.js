import React from 'react';
import './Navbar.css';

const Navbar = ({ currentView, setCurrentView }) => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-logo">
          <span className="logo-icon">🔐</span>
          <span className="logo-text">The Cipher Academy</span>
        </div>
        
        <div className="nav-menu">
          <button 
            className={`nav-link ${currentView === 'home' ? 'active' : ''}`}
            onClick={() => setCurrentView('home')}
          >
            Home
          </button>
          <button 
            className={`nav-link ${currentView === 'about' ? 'active' : ''}`}
            onClick={() => setCurrentView('about')}
          >
            About
          </button>
          <button 
            className={`nav-link ${currentView === 'contact' ? 'active' : ''}`}
            onClick={() => setCurrentView('contact')}
          >
            Contact
          </button>
          <button className="nav-cta">
            Begin Journey
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
