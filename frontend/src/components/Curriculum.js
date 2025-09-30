import React, { useState } from 'react';
import './Curriculum.css';

const Curriculum = () => {
  const [activeEra, setActiveEra] = useState(0);

  const eras = [
    {
      title: 'Ancient Foundations',
      period: 'Weeks 1-12',
      timespan: '3000 BCE - 500 CE',
      difficulty: '1-6',
      color: '#8B4513',
      description: 'Master the cryptographic techniques that built civilizations',
      techniques: [
        'Spartan Scytale - Ancient military communications',
        'Caesar Cipher - Roman imperial security',
        'Atbash Cipher - Hebrew scribal traditions',
        'Polybius Square - Greek tactical signaling',
        'Alberti Disk - Renaissance polyalphabetic innovation'
      ],
      highlights: [
        'Learn how ancient armies secured their communications',
        'Discover the mathematical foundations of substitution ciphers',
        'Explore the role of cryptography in religious texts'
      ]
    },
    {
      title: 'Renaissance Revolution',
      period: 'Weeks 13-30',
      timespan: '1400 - 1700 CE',
      difficulty: '7-10',
      color: '#DAA520',
      description: 'Experience the golden age of cryptographic innovation',
      techniques: [
        'Vigenère Cipher - The "unbreakable" polyalphabetic system',
        'Playfair Cipher - Digraph substitution advancement',
        'Four-Square Cipher - Multi-layer encryption',
        'Great Cipher - Louis XIV\'s diplomatic security',
        'Bacon\'s Binary - Early steganographic methods'
      ],
      highlights: [
        'Study the ciphers that protected royal correspondence',
        'Understand the mathematical evolution of encryption',
        'Learn techniques that influenced modern cryptography'
      ]
    },
    {
      title: 'Industrial Innovation',
      period: 'Weeks 31-60',
      timespan: '1800 - 1945 CE',
      difficulty: '11-15',
      color: '#2E8B57',
      description: 'Navigate the mechanization of secret communications',
      techniques: [
        'Telegraph Codes - Commercial and military applications',
        'Enigma Machine - WWII German encryption device',
        'Purple Cipher - Japanese diplomatic security',
        'Colossus Computer - Early electronic code-breaking',
        'One-Time Pad - Information-theoretic security'
      ],
      highlights: [
        'Explore how mechanical devices revolutionized encryption',
        'Study the codebreaking efforts that changed history',
        'Understand the birth of modern cryptanalysis'
      ]
    },
    {
      title: 'Modern Warfare',
      period: 'Weeks 61-80',
      timespan: '1945 - 1990 CE',
      difficulty: '16-18',
      color: '#4169E1',
      description: 'Master the computer age of cryptographic warfare',
      techniques: [
        'DES Algorithm - Data Encryption Standard',
        'RSA Encryption - Public-key cryptography revolution',
        'Diffie-Hellman - Key exchange protocols',
        'AES Development - Advanced Encryption Standard',
        'Hash Functions - Digital signature foundations'
      ],
      highlights: [
        'Learn the mathematical foundations of modern encryption',
        'Understand public-key cryptography principles',
        'Explore the standardization of cryptographic systems'
      ]
    },
    {
      title: 'Digital Future',
      period: 'Weeks 81-91',
      timespan: '1990 - Present',
      difficulty: '19-20',
      color: '#9400D3',
      description: 'Prepare for the quantum cryptographic frontier',
      techniques: [
        'Elliptic Curve Cryptography - Efficient modern encryption',
        'Quantum Key Distribution - Unconditional security',
        'Post-Quantum Cryptography - Quantum-resistant algorithms',
        'Blockchain Cryptography - Distributed ledger security',
        'Homomorphic Encryption - Computing on encrypted data'
      ],
      highlights: [
        'Explore cutting-edge cryptographic research',
        'Understand quantum computing threats and opportunities',
        'Prepare for the future of secure communications'
      ]
    }
  ];

  return (
    <section className="curriculum">
      <div className="curriculum-container">
        <div className="curriculum-header">
          <h2>Your 21-Month Cryptographic Journey</h2>
          <p>5,000 years of secret communications, progressively mastered</p>
        </div>

        <div className="era-navigation">
          {eras.map((era, index) => (
            <button
              key={index}
              className={`era-tab ${activeEra === index ? 'active' : ''}`}
              onClick={() => setActiveEra(index)}
              style={{ borderColor: era.color }}
            >
              <span className="era-title">{era.title}</span>
              <span className="era-period">{era.period}</span>
            </button>
          ))}
        </div>

        <div className="era-content">
          {eras.map((era, index) => (
            <div
              key={index}
              className={`era-panel ${activeEra === index ? 'active' : ''}`}
            >
              <div className="era-info">
                <div className="era-header-info">
                  <h3 style={{ color: era.color }}>{era.title}</h3>
                  <div className="era-metadata">
                    <span className="timespan">{era.timespan}</span>
                    <span className="difficulty">Difficulty: {era.difficulty}/20</span>
                  </div>
                </div>
                <p className="era-description">{era.description}</p>
              </div>

              <div className="era-details">
                <div className="techniques-section">
                  <h4>Key Techniques You'll Master</h4>
                  <ul className="techniques-list">
                    {era.techniques.map((technique, idx) => (
                      <li key={idx}>{technique}</li>
                    ))}
                  </ul>
                </div>

                <div className="highlights-section">
                  <h4>Learning Highlights</h4>
                  <ul className="highlights-list">
                    {era.highlights.map((highlight, idx) => (
                      <li key={idx}>{highlight}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="curriculum-stats">
          <div className="stat-card">
            <span className="stat-number">273</span>
            <span className="stat-label">Total Challenges</span>
            <span className="stat-detail">3 per week for 91 weeks</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">54</span>
            <span className="stat-label">Visual Puzzles</span>
            <span className="stat-detail">20% image-based challenges</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">20</span>
            <span className="stat-label">Difficulty Levels</span>
            <span className="stat-detail">Progressive skill building</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">5000+</span>
            <span className="stat-label">Years Covered</span>
            <span className="stat-detail">Ancient to quantum era</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Curriculum;
