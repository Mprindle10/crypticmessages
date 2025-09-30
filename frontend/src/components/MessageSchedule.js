import React, { useState, useEffect } from 'react';
import './MessageSchedule.css';

const MessageSchedule = ({ userId }) => {
  const [currentWeek, setCurrentWeek] = useState(1);
  const [userProgress, setUserProgress] = useState(null);
  const [weeklyMessages, setWeeklyMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserProgress();
    fetchWeeklyMessages();
  }, [userId, currentWeek]);

  const fetchUserProgress = async () => {
    try {
      const response = await fetch(`/api/user-progress/${userId}`);
      const data = await response.json();
      setUserProgress(data);
      setCurrentWeek(data.current_week);
    } catch (error) {
      console.error('Error fetching user progress:', error);
    }
  };

  const fetchWeeklyMessages = async () => {
    try {
      const response = await fetch(`/api/messages/week/${currentWeek}`);
      const data = await response.json();
      setWeeklyMessages(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching weekly messages:', error);
      setLoading(false);
    }
  };

  const getMessageStatusIcon = (dayOfWeek, isCompleted) => {
    if (isCompleted) return '✅';
    
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    const messageDay = dayOfWeek;
    
    if (today === messageDay) return '🎯'; // Current day
    if (['Sunday', 'Wednesday', 'Friday'].indexOf(today) > 
        ['Sunday', 'Wednesday', 'Friday'].indexOf(messageDay)) return '📬'; // Available
    return '🔒'; // Locked
  };

  const getDayColor = (dayOfWeek, isCompleted) => {
    if (isCompleted) return 'completed';
    
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    if (today === dayOfWeek) return 'current';
    if (['Sunday', 'Wednesday', 'Friday'].indexOf(today) > 
        ['Sunday', 'Wednesday', 'Friday'].indexOf(dayOfWeek)) return 'available';
    return 'locked';
  };

  if (loading) {
    return <div className="loading">Loading your cryptic journey...</div>;
  }

  return (
    <div className="message-schedule">
      <div className="week-header">
        <h2>Week {currentWeek} - Cryptic Challenge Schedule</h2>
        <div className="progress-stats">
          <span>Solved: {userProgress?.total_solved || 0}</span>
          <span>Streak: {userProgress?.current_streak || 0}</span>
          <span>Points: {userProgress?.total_points || 0}</span>
        </div>
      </div>

      <div className="weekly-grid">
        {weeklyMessages.map((message) => (
          <div 
            key={message.id}
            className={`message-card ${getDayColor(message.day_of_week, message.is_completed)}`}
          >
            <div className="message-header">
              <span className="day-label">{message.day_of_week}</span>
              <span className="status-icon">
                {getMessageStatusIcon(message.day_of_week, message.is_completed)}
              </span>
            </div>
            
            <h3 className="message-title">{message.title}</h3>
            
            <div className="message-preview">
              {message.is_completed ? 
                `Solution: ${message.user_solution}` : 
                `${message.message.substring(0, 100)}...`
              }
            </div>
            
            <div className="message-meta">
              <span className="difficulty">Level {message.difficulty_level}</span>
              <span className="points">{message.reward_points} pts</span>
            </div>
            
            {message.day_of_week === new Date().toLocaleDateString('en-US', { weekday: 'long' }) && (
              <button className="solve-button">
                Solve Today's Challenge
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="delivery-schedule">
        <h3>📅 Message Delivery Schedule</h3>
        <div className="schedule-info">
          <div className="schedule-item">
            <span className="day">🌅 Sunday</span>
            <span className="time">8:00 AM</span>
            <span className="type">Week Opener</span>
          </div>
          <div className="schedule-item">
            <span className="day">🌙 Wednesday</span>
            <span className="time">6:00 PM</span>
            <span className="type">Mid-Week Challenge</span>
          </div>
          <div className="schedule-item">
            <span className="day">🎉 Friday</span>
            <span className="time">3:00 PM</span>
            <span className="type">Week Closer</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageSchedule;
