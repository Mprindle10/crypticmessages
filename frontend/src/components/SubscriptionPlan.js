import React, { useState } from 'react';
import './SubscriptionPlan.css';

const SubscriptionPlan = () => {
  const [selectedPlan, setSelectedPlan] = useState('monthly');
  const [loading, setLoading] = useState(false);

  const plans = {
    monthly: {
      name: 'Monthly Cryptic Adventure',
      price: 9.99,
      duration: '1 month',
      messages: 12,
      description: 'Perfect for trying out our cryptic challenge experience',
      features: [
        '3 messages per week (Sun/Wed/Fri)',
        'Progressive difficulty levels',
        'SMS & Email delivery',
        'Solution tracking',
        'Hint system',
        'Cancel anytime'
      ]
    },
    quarterly: {
      name: 'Quarterly Cipher Quest',
      price: 24.99,
      duration: '3 months',
      messages: 36,
      description: 'Dive deeper into the world of cryptic puzzles',
      features: [
        '3 messages per week (Sun/Wed/Fri)',
        'Advanced cipher techniques',
        'SMS & Email delivery',
        'Progress analytics',
        'Bonus weekend challenges',
        '15% savings vs monthly'
      ]
    },
    annual: {
      name: 'Annual Master Cryptographer',
      price: 89.99,
      duration: '12 months',
      messages: 156,
      description: 'Complete cryptographic mastery journey',
      features: [
        '3 messages per week (Sun/Wed/Fri)',
        'Expert-level challenges',
        'SMS & Email delivery',
        'Detailed progress tracking',
        'Exclusive cipher tools',
        'VIP support',
        '25% savings vs monthly'
      ]
    },
    ultimate: {
      name: 'Ultimate 21-Month Journey',
      price: 149.99,
      duration: '21 months',
      messages: 273,
      description: 'The complete cryptic message experience',
      features: [
        '3 messages per week (Sun/Wed/Fri)',
        'Complete curriculum progression',
        'SMS & Email delivery',
        'Master cryptographer certificate',
        'Exclusive community access',
        'Lifetime achievement tracking',
        'Best value - 30% savings'
      ]
    }
  };

  const handleSubscribe = async (planType) => {
    setLoading(true);
    
    try {
      const response = await fetch('/api/create-subscription', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plan: planType,
          email: 'user@example.com', // Replace with actual user email
          phone: '+1234567890' // Replace with actual user phone
        }),
      });

      const data = await response.json();
      
      if (data.client_secret) {
        // Redirect to Stripe payment page
        window.location.href = `/payment?client_secret=${data.client_secret}&plan=${planType}`;
      }
    } catch (error) {
      console.error('Subscription error:', error);
      alert('Error creating subscription. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getMessageFrequency = (messages) => {
    const weeks = Math.ceil(messages / 3);
    return `${weeks} weeks of tri-weekly challenges`;
  };

  return (
    <div className="subscription-plan">
      <div className="plan-header">
        <h1>Choose Your Cryptic Journey</h1>
        <p>Unlock the mysteries with our progressive cryptic message challenges</p>
      </div>

      <div className="delivery-info">
        <h3>📅 Message Delivery Schedule</h3>
        <div className="delivery-grid">
          <div className="delivery-item">
            <span className="emoji">🌅</span>
            <div>
              <strong>Sunday Morning</strong>
              <p>Week opener - Sets the theme</p>
            </div>
          </div>
          <div className="delivery-item">
            <span className="emoji">🌙</span>
            <div>
              <strong>Wednesday Evening</strong>
              <p>Mid-week challenge - Builds complexity</p>
            </div>
          </div>
          <div className="delivery-item">
            <span className="emoji">🎉</span>
            <div>
              <strong>Friday Afternoon</strong>
              <p>Week closer - Combines learning</p>
            </div>
          </div>
        </div>
      </div>

      <div className="plans-grid">
        {Object.entries(plans).map(([key, plan]) => (
          <div 
            key={key}
            className={`plan-card ${selectedPlan === key ? 'selected' : ''} ${key === 'ultimate' ? 'featured' : ''}`}
            onClick={() => setSelectedPlan(key)}
          >
            {key === 'ultimate' && <div className="featured-badge">🎯 Most Popular</div>}
            
            <div className="plan-header-card">
              <h3>{plan.name}</h3>
              <div className="price">
                <span className="currency">$</span>
                <span className="amount">{plan.price}</span>
                <span className="period">/{plan.duration}</span>
              </div>
            </div>

            <p className="plan-description">{plan.description}</p>

            <div className="plan-stats">
              <div className="stat">
                <strong>{plan.messages}</strong>
                <span>Total Messages</span>
              </div>
              <div className="stat">
                <strong>{getMessageFrequency(plan.messages)}</strong>
                <span>Duration</span>
              </div>
            </div>

            <ul className="features-list">
              {plan.features.map((feature, index) => (
                <li key={index}>
                  <span className="checkmark">✓</span>
                  {feature}
                </li>
              ))}
            </ul>

            <button 
              className={`subscribe-btn ${selectedPlan === key ? 'selected' : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                handleSubscribe(key);
              }}
              disabled={loading}
            >
              {loading ? 'Processing...' : `Subscribe to ${plan.name}`}
            </button>
          </div>
        ))}
      </div>

      <div className="guarantee">
        <h3>🛡️ 30-Day Money-Back Guarantee</h3>
        <p>Not satisfied with your cryptic adventure? Get a full refund within 30 days, no questions asked.</p>
      </div>
    </div>
  );
};

export default SubscriptionPlan;
