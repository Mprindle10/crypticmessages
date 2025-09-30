import React from 'react';
import './Features.css';

const Features = () => {
  const features = [
    {
      icon: '🏛️',
      title: 'Educational Excellence',
      description: 'University-level cryptographic curriculum spanning 91 weeks',
      details: [
        'Progressive difficulty from beginner (Level 1) to expert (Level 20)',
        'Historically accurate content covering every major cryptographic era',
        'Learn from ancient Spartans to quantum computers'
      ]
    },
    {
      icon: '🧩',
      title: 'Interactive Learning',
      description: 'Tri-weekly challenges requiring previous week\'s solutions',
      details: [
        '20% visual puzzles with historically-inspired imagery',
        'Immediate feedback and hint system',
        'Each puzzle builds on previous knowledge'
      ]
    },
    {
      icon: '📱',
      title: 'Multi-Channel Delivery',
      description: 'SMS delivery via Twilio for instant access',
      details: [
        'Email delivery with rich formatting',
        'Progressive web app for progress tracking',
        'Never miss a challenge with dual delivery'
      ]
    },
    {
      icon: '🎯',
      title: 'Structured Progression',
      description: 'Journey through 5,000 years of cryptographic history',
      details: [
        'Ancient Foundations: Scytale, Caesar, Atbash',
        'Renaissance Revolution: Vigenère, Alberti, Playfair',
        'Modern Warfare: Enigma, Purple, Computer Ciphers',
        'Digital Future: RSA, Quantum Cryptography'
      ]
    }
  ];

  const deliverySchedule = [
    { day: 'Sunday', time: '8:00 AM', description: 'Week opener challenge', icon: '🌅' },
    { day: 'Wednesday', time: '6:00 PM', description: 'Mid-week progression', icon: '🌙' },
    { day: 'Friday', time: '3:00 PM', description: 'Week completion challenge', icon: '🎉' }
  ];

  return (
    <section className="features">
      <div className="features-container">
        <div className="features-header">
          <h2>Why Choose The Cipher Academy Journey?</h2>
          <p>The most comprehensive cryptographic education ever created</p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
              <ul className="feature-details">
                {feature.details.map((detail, idx) => (
                  <li key={idx}>{detail}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="delivery-schedule">
          <h3>Tri-Weekly Delivery Schedule</h3>
          <div className="schedule-grid">
            {deliverySchedule.map((schedule, index) => (
              <div key={index} className="schedule-card">
                <div className="schedule-icon">{schedule.icon}</div>
                <div className="schedule-info">
                  <h4>{schedule.day}</h4>
                  <span className="schedule-time">{schedule.time}</span>
                  <p>{schedule.description}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="schedule-note">
            Each message requires the previous week's solution, creating an interconnected 
            learning experience that mirrors how cryptographic knowledge actually developed.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Features;
