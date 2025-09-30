import React from 'react';
import './Testimonials.css';

const Testimonials = () => {
  const testimonials = [
    {
      quote: "The Cipher Academy Journey transformed my understanding of cybersecurity. Learning historical cryptanalysis made me a better penetration tester.",
      author: "Sarah Chen",
      role: "Cybersecurity Professional",
      company: "SecureNet Solutions",
      avatar: "👩‍💻",
      rating: 5
    },
    {
      quote: "As a computer science professor, I use these historical examples in my classes. My students are fascinated by the progression from ancient ciphers to modern encryption.",
      author: "Dr. Michael Rodriguez",
      role: "CS Professor",
      company: "Stanford University",
      avatar: "👨‍🏫",
      rating: 5
    },
    {
      quote: "I've always loved puzzles, but this took it to another level. Each challenge builds on the last, creating an incredible learning experience.",
      author: "Emma Thompson",
      role: "Escape Room Enthusiast",
      company: "Software Engineer",
      avatar: "🧩",
      rating: 5
    },
    {
      quote: "The tri-weekly format is perfect for busy professionals. I look forward to each challenge and the historical context makes it so much more engaging.",
      author: "David Kim",
      role: "IT Security Manager",
      company: "TechCorp Industries",
      avatar: "👨‍💼",
      rating: 5
    },
    {
      quote: "From Caesar ciphers to quantum cryptography - this journey covers everything. The visual puzzles are particularly well-designed and historically accurate.",
      author: "Dr. Lisa Wang",
      role: "Cryptography Researcher",
      company: "MIT",
      avatar: "👩‍🔬",
      rating: 5
    },
    {
      quote: "Perfect for self-paced learning. The difficulty progression is spot-on, and the community aspect adds so much value to the experience.",
      author: "James Mitchell",
      role: "Lifelong Learner",
      company: "Retired Engineer",
      avatar: "📚",
      rating: 5
    }
  ];

  const targetAudiences = [
    {
      title: "The Academic Enthusiast",
      icon: "🎓",
      description: "History/Math/CS students and professors",
      traits: [
        "Values intellectual challenge and historical accuracy",
        "Willing to pay premium for quality educational content",
        "Seeks deep understanding of cryptographic foundations"
      ]
    },
    {
      title: "The Cybersecurity Professional",
      icon: "🔐",
      description: "IT security specialists and penetration testers",
      traits: [
        "Seeks to understand cryptographic foundations",
        "Appreciates hands-on problem-solving approach",
        "Values practical applications in modern security"
      ]
    },
    {
      title: "The Puzzle Lover",
      icon: "🧠",
      description: "Escape room enthusiasts and puzzle gamers",
      traits: [
        "Enjoys progressive difficulty and achievement systems",
        "Attracted to mysterious and challenging content",
        "Loves interconnected puzzle experiences"
      ]
    },
    {
      title: "The Lifelong Learner",
      icon: "📚",
      description: "Curious adults seeking intellectual stimulation",
      traits: [
        "Appreciates structured learning with flexibility",
        "Values education as entertainment",
        "Enjoys exploring historical contexts"
      ]
    }
  ];

  return (
    <section className="testimonials">
      <div className="testimonials-container">
        <div className="testimonials-header">
          <h2>Join Thousands of Cryptography Enthusiasts</h2>
          <p>Hear from our community of learners, professionals, and puzzle solvers</p>
        </div>

        <div className="testimonials-grid">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="testimonial-card">
              <div className="testimonial-content">
                <div className="rating">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <span key={i} className="star">⭐</span>
                  ))}
                </div>
                <blockquote>"{testimonial.quote}"</blockquote>
              </div>
              
              <div className="testimonial-author">
                <div className="author-avatar">{testimonial.avatar}</div>
                <div className="author-info">
                  <div className="author-name">{testimonial.author}</div>
                  <div className="author-role">{testimonial.role}</div>
                  <div className="author-company">{testimonial.company}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="audience-section">
          <h3>Perfect For Every Type of Learner</h3>
          <div className="audience-grid">
            {targetAudiences.map((audience, index) => (
              <div key={index} className="audience-card">
                <div className="audience-icon">{audience.icon}</div>
                <h4>{audience.title}</h4>
                <p className="audience-description">{audience.description}</p>
                <ul className="audience-traits">
                  {audience.traits.map((trait, idx) => (
                    <li key={idx}>{trait}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="social-proof">
          <div className="proof-stats">
            <div className="proof-stat">
              <span className="proof-number">2,847</span>
              <span className="proof-label">Active Subscribers</span>
            </div>
            <div className="proof-stat">
              <span className="proof-number">4.9/5</span>
              <span className="proof-label">Average Rating</span>
            </div>
            <div className="proof-stat">
              <span className="proof-number">89%</span>
              <span className="proof-label">Complete Full Journey</span>
            </div>
            <div className="proof-stat">
              <span className="proof-number">156</span>
              <span className="proof-label">Universities Using</span>
            </div>
          </div>
        </div>

        <div className="community-benefits">
          <h3>Beyond Just Learning - Join Our Community</h3>
          <div className="benefits-grid">
            <div className="benefit-item">
              <span className="benefit-icon">💬</span>
              <h4>Discussion Forums</h4>
              <p>Connect with fellow cryptography enthusiasts and share insights</p>
            </div>
            <div className="benefit-item">
              <span className="benefit-icon">🏆</span>
              <h4>Leaderboards</h4>
              <p>Compete with others and track your progress through the curriculum</p>
            </div>
            <div className="benefit-item">
              <span className="benefit-icon">📖</span>
              <h4>Additional Resources</h4>
              <p>Access bonus materials, historical documentaries, and research papers</p>
            </div>
            <div className="benefit-item">
              <span className="benefit-icon">🎓</span>
              <h4>Certificates</h4>
              <p>Earn completion certificates for each era and the full journey</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
