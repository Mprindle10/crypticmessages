import React, { useState, useEffect } from 'react';
import './youtube_short_animations.css';

const YouTubeShortPreview = () => {
  const [currentLetter, setCurrentLetter] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [particles, setParticles] = useState([]);

  const originalText = "HELLO";
  const encryptedText = "KHOOR";
  const letters = ["H", "E", "L", "L", "O"];
  const shiftedLetters = ["K", "H", "O", "O", "R"];

  useEffect(() => {
    // Initialize particles
    const newParticles = Array.from({ length: 9 }, (_, i) => ({
      id: i,
      delay: i * 0.5
    }));
    setParticles(newParticles);

    // Animation sequence
    const sequence = async () => {
      await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for scroll animation
      
      // Show letters one by one
      for (let i = 0; i < letters.length; i++) {
        setCurrentLetter(i + 1);
        await new Promise(resolve => setTimeout(resolve, 800));
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      setShowAnswer(true);
    };

    sequence();
  }, []);

  const generateAlphabetWheel = () => {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return alphabet.split('').map((letter, index) => (
      <div key={index} className="wheel-letter">
        {letter}
      </div>
    ));
  };

  return (
    <div className="youtube-short-preview">
      {/* Ancient Scroll Background */}
      <div className="ancient-scroll" />
      
      {/* Particles */}
      <div className="particles-container">
        {particles.map(particle => (
          <div
            key={particle.id}
            className="particle"
            style={{ animationDelay: `${particle.delay}s` }}
          />
        ))}
      </div>

      {/* Hook Badge */}
      <div className="genius-test-badge">
        🧠 GENIUS TEST
      </div>

      {/* Main Cipher Display */}
      <div className="cipher-display">
        <div className="encrypted-text">
          {encryptedText.split('').map((letter, index) => (
            <span
              key={index}
              className={`letter-shift ${index < currentLetter ? 'animate' : ''}`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {letter}
            </span>
          ))}
        </div>

        {showAnswer && (
          <div className="success-reveal">
            ✨ {originalText} ✨
          </div>
        )}
      </div>

      {/* Alphabet Wheel */}
      <div className="alphabet-wheel">
        A→D
      </div>

      {/* Challenge Hint */}
      <div className="challenge-hint">
        Each letter shifts by 3!
      </div>

      {/* Call to Action */}
      <button 
        className="cta-button"
        onClick={() => window.open('http://localhost:8000/beta', '_blank')}
      >
        🧩 START SOLVING
      </button>
    </div>
  );
};

export default YouTubeShortPreview;
