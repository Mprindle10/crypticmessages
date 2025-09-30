import React from 'react';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-logo">
              <span className="logo-icon">🔐</span>
              <span className="logo-text">The Cipher Academy</span>
            </div>
            <p className="footer-description">
              Master 5,000 years of cryptographic history through progressive, 
              tri-weekly challenges. From ancient Spartan scytales to quantum cryptography.
            </p>
            <div className="footer-social">
              <a href="#" className="social-link">📧</a>
              <a href="#" className="social-link">🐦</a>
              <a href="#" className="social-link">💼</a>
              <a href="#" className="social-link">📘</a>
            </div>
          </div>

          <div className="footer-section">
            <h4>Learning Paths</h4>
            <ul className="footer-links">
              <li><a href="#ancient">Ancient Foundations</a></li>
              <li><a href="#renaissance">Renaissance Revolution</a></li>
              <li><a href="#industrial">Industrial Innovation</a></li>
              <li><a href="#modern">Modern Warfare</a></li>
              <li><a href="#digital">Digital Future</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Resources</h4>
            <ul className="footer-links">
              <li><a href="#blog">Blog</a></li>
              <li><a href="#documentation">Documentation</a></li>
              <li><a href="#community">Community Forum</a></li>
              <li><a href="#support">Support Center</a></li>
              <li><a href="#certificates">Certificates</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Company</h4>
            <ul className="footer-links">
              <li><a href="#about">About Us</a></li>
              <li><a href="#careers">Careers</a></li>
              <li><a href="#partnerships">Partnerships</a></li>
              <li><a href="#press">Press Kit</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Newsletter</h4>
            <p>Get weekly cryptographic insights and bonus challenges</p>
            <form className="newsletter-form">
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="newsletter-input"
              />
              <button type="submit" className="newsletter-button">
                Subscribe
              </button>
            </form>
            <p className="newsletter-note">
              🔐 Free cipher challenges • Historical insights • No spam
            </p>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-legal">
            <p>&copy; {currentYear} The Cipher Academy. All rights reserved.</p>
            <div className="legal-links">
              <a href="#privacy">Privacy Policy</a>
              <a href="#terms">Terms of Service</a>
              <a href="#cookies">Cookie Policy</a>
            </div>
          </div>
          
          <div className="footer-features">
            <span className="feature-badge">🛡️ Secure Learning</span>
            <span className="feature-badge">📱 Mobile Friendly</span>
            <span className="feature-badge">🎓 University Approved</span>
          </div>
        </div>

        <div className="footer-testimonial">
          <blockquote>
            "The most comprehensive cryptographic education I've ever encountered. 
            Every cybersecurity professional should take this journey."
          </blockquote>
          <cite>— Dr. Elena Vasquez, CISSP, Security Architect</cite>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
