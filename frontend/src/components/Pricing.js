import React, { useState } from 'react';
import './Pricing.css';

const Pricing = () => {
  const [selectedPlan, setSelectedPlan] = useState('full');

  const plans = [
    {
      id: 'sampler',
      name: 'Monthly Sampler',
      price: '$19.99',
      period: '/month',
      description: 'Experience any current month of content',
      features: [
        'Current month\'s 12-13 challenges',
        'SMS and Email delivery',
        'Basic progress tracking',
        'Access to hints and solutions',
        'Cancel anytime, resume later'
      ],
      cta: 'Start Monthly Trial',
      badge: null,
      color: '#6c757d'
    },
    {
      id: 'era',
      name: 'Era Explorer',
      price: '$89',
      period: 'one-time',
      description: 'Focus on specific historical periods',
      features: [
        'Choose any complete era (3-6 months)',
        '39-78 messages depending on era',
        'Full visual puzzle collection for era',
        'Detailed historical context',
        'Perfect for targeted learning interests'
      ],
      cta: 'Choose Your Era',
      badge: 'Popular',
      color: '#ffc107'
    },
    {
      id: 'full',
      name: 'Full Academy Journey',
      price: '$297',
      period: '$14/month for 21 months',
      description: 'Complete 273-message curriculum',
      features: [
        'All 273 cryptographic challenges',
        'Complete 91-week journey',
        'All 54 visual puzzles and interactive content',
        'Progress tracking and achievement system',
        'Premium support and community access',
        'Lifetime access to completed content'
      ],
      cta: 'Begin Full Journey',
      badge: 'Best Value',
      color: '#28a745'
    }
  ];

  const handleSelectPlan = (planId) => {
    setSelectedPlan(planId);
  };

  const handleSubscribe = async (plan) => {
    try {
      // TODO: Integrate with Stripe for payment processing
      console.log('Starting subscription for:', plan.name);
      
      if (plan.id === 'sampler') {
        // Monthly subscription flow
        window.location.href = `/checkout?plan=monthly&price=1999`;
      } else if (plan.id === 'era') {
        // One-time payment flow
        window.location.href = `/checkout?plan=era&price=8900`;
      } else if (plan.id === 'full') {
        // Full journey subscription flow
        window.location.href = `/checkout?plan=full&price=29700&installments=21`;
      }
      
      // Alternative: Open Stripe Checkout modal
      // const stripe = await stripePromise;
      // const { error } = await stripe.redirectToCheckout({
      //   sessionId: checkoutSession.id,
      // });
      
    } catch (error) {
      console.error('Subscription error:', error);
      alert('Unable to process subscription. Please try again.');
    }
  };

  return (
    <section className="pricing">
      <div className="pricing-container">
        <div className="pricing-header">
          <h2>Choose Your Cryptographic Journey</h2>
          <p>Flexible plans to match your learning goals and timeline</p>
        </div>

        <div className="pricing-grid">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`pricing-card ${selectedPlan === plan.id ? 'selected' : ''}`}
              onClick={() => handleSelectPlan(plan.id)}
            >
              {plan.badge && (
                <div className="plan-badge" style={{ backgroundColor: plan.color }}>
                  {plan.badge}
                </div>
              )}
              
              <div className="plan-header">
                <h3>{plan.name}</h3>
                <div className="plan-price">
                  <span className="price">{plan.price}</span>
                  <span className="period">{plan.period}</span>
                </div>
                <p className="plan-description">{plan.description}</p>
              </div>

              <div className="plan-features">
                <ul>
                  {plan.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>

              <button
                className="plan-cta"
                style={{ backgroundColor: plan.color }}
                onClick={(e) => {
                  e.stopPropagation();
                  handleSubscribe(plan);
                }}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        <div className="pricing-comparison">
          <h3>Why The Full Journey?</h3>
          <div className="comparison-grid">
            <div className="comparison-point">
              <span className="comparison-icon">💰</span>
              <h4>Best Value</h4>
              <p>$14/month vs $20/month for individual content</p>
            </div>
            <div className="comparison-point">
              <span className="comparison-icon">🎯</span>
              <h4>Complete Experience</h4>
              <p>Designed as interconnected learning journey</p>
            </div>
            <div className="comparison-point">
              <span className="comparison-icon">🏆</span>
              <h4>Achievement System</h4>
              <p>Track progress across entire cryptographic history</p>
            </div>
            <div className="comparison-point">
              <span className="comparison-icon">👥</span>
              <h4>Community Access</h4>
              <p>Connect with fellow cryptography enthusiasts</p>
            </div>
          </div>
        </div>

        <div className="pricing-faq">
          <h3>Frequently Asked Questions</h3>
          <div className="faq-grid">
            <div className="faq-item">
              <h4>Can I switch plans later?</h4>
              <p>Yes! You can upgrade to the Full Journey at any time and get credit for what you've already paid.</p>
            </div>
            <div className="faq-item">
              <h4>What if I miss a challenge?</h4>
              <p>No worries! All content remains accessible, and you can catch up at your own pace.</p>
            </div>
            <div className="faq-item">
              <h4>Do I need prior cryptography knowledge?</h4>
              <p>Not at all! We start from the very beginning with ancient techniques and build up progressively.</p>
            </div>
            <div className="faq-item">
              <h4>Is there a money-back guarantee?</h4>
              <p>Yes! 30-day full refund if you're not completely satisfied with your experience.</p>
            </div>
          </div>
        </div>

        <div className="pricing-testimonial">
          <blockquote>
            "The Cipher Academy Journey transformed my understanding of cybersecurity. 
            Learning historical cryptanalysis made me a better penetration tester."
          </blockquote>
          <cite>— Sarah Chen, Cybersecurity Professional</cite>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
