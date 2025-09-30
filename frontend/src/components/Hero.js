import React, { useState } from 'react';
import './Hero.css';

const Hero = () => {
  const [email, setEmail] = useState('');
  const [isSubscribed, setIsSubscribed] = useState(false);

  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (email) {
      try {
        // TODO: Replace with your actual API endpoint
        const response = await fetch('/api/subscribe', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            email: email,
            plan: 'free_trial',
            source: 'hero_signup'
          }),
        });

        if (response.ok) {
          setIsSubscribed(true);
          // TODO: Send to your email service (SendGrid)
          // TODO: Add to your database
          // TODO: Send welcome email with first challenge
          console.log('Successfully subscribed:', email);
        } else {
          console.error('Subscription failed:', response.statusText);
          alert('Subscription failed. Please try again.');
        }
      } catch (error) {
        console.error('Subscription error:', error);
        alert('Network error. Please check your connection and try again.');
      }
    }
  };

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Master the Art of <span className="highlight">Secret Messages</span>
            </h1>
            <p className="hero-subtitle">
              From Ancient Codes to Quantum Cryptography - A 21-Month Journey Through Cryptographic History
            </p>
            <p className="hero-description">
              Every great cipher tells a story. The Spartan scytale that secured military communications. 
              The Enigma machine that nearly won WWII. The RSA algorithm that protects your online banking.
            </p>
            <p className="hero-cta-text">
              Now it's your turn to learn these legendary techniques.
            </p>
            
            {!isSubscribed ? (
              <form className="hero-form" onSubmit={handleSubscribe}>
                <div className="input-group">
                  <input
                    type="email"
                    placeholder="Enter your email to begin..."
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="hero-input"
                    required
                  />
                  <button type="submit" className="hero-button">
                    Begin Your Academy Journey
                  </button>
                </div>
                <p className="hero-promise">
                  🔐 Start with Week 1 FREE • No credit card required
                </p>
              </form>
            ) : (
              <div className="success-message">
                <h3>🎉 Welcome to The Cipher Academy!</h3>
                <p>Check your email for your first cryptographic challenge.</p>
              </div>
            )}
          </div>
          
          <div className="hero-visual">
            <div className="cipher-wheel">
              <div className="wheel-outer">
                <div className="wheel-inner">
                  <span className="wheel-text">🔐</span>
                </div>
              </div>
              <div className="floating-symbols">
                <span className="symbol symbol-1">⚡</span>
                <span className="symbol symbol-2">🗝️</span>
                <span className="symbol symbol-3">📜</span>
                <span className="symbol symbol-4">🔍</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">273</span>
            <span className="stat-label">Unique Challenges</span>
          </div>
          <div className="stat">
            <span className="stat-number">91</span>
            <span className="stat-label">Weeks of Learning</span>
          </div>
          <div className="stat">
            <span className="stat-number">5000+</span>
            <span className="stat-label">Years of History</span>
          </div>
          <div className="stat">
            <span className="stat-number">20</span>
            <span className="stat-label">Difficulty Levels</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
