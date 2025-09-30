"""
SQLAlchemy Models for Cryptic Messages Service
Database models matching your PostgreSQL schema
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """User model for subscribers"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    subscription_type = Column(String(50), default="free_trial")
    signup_source = Column(String(100))
    phone = Column(String(20))
    experience = Column(String(100))  # User's cryptography experience level
    motivation = Column(Text)  # Why they want to learn cryptography
    background = Column(Text)  # User's background/profession
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)
    current_week = Column(Integer, default=1)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    subscription_id = Column(String(255))  # Stripe subscription ID
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user", uselist=False)
    submissions = relationship("UserSubmission", back_populates="user")
    welcome_emails = relationship("UserWelcomeEmail", back_populates="user")

class CrypticMessage(Base):
    """Cryptic message challenges"""
    __tablename__ = "cryptic_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, nullable=False, index=True)
    day_of_week = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    answer = Column(String(255), nullable=False)
    difficulty_level = Column(Integer, default=1)
    points_value = Column(Integer, default=10)
    hint = Column(Text)
    cipher_type = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships (removed submissions relationship until proper FK is added)

class UserProgress(Base):
    """User progress tracking"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    current_week = Column(Integer, default=1)
    total_solved = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress")

class UserSubmission(Base):
    """User challenge submissions"""
    __tablename__ = "user_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    user_answer = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)
    hint_used = Column(Boolean, default=False)
    submitted_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    # challenge relationship removed until proper FK column is added

class EmailTemplate(Base):
    """Email templates for welcome series"""
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(255), nullable=False)
    email_sequence = Column(Integer, nullable=False)
    subject_line = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=False)
    plain_text_content = Column(Text, nullable=False)
    days_after_signup = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user_emails = relationship("UserWelcomeEmail", back_populates="template")

class UserWelcomeEmail(Base):
    """User welcome email tracking"""
    __tablename__ = "user_welcome_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    status = Column(String(50), default="scheduled")  # scheduled, sent, delivered, opened, clicked
    sendgrid_message_id = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="welcome_emails")
    template = relationship("EmailTemplate", back_populates="user_emails")

class IncorrectAttempt(Base):
    """Track incorrect attempts for analytics"""
    __tablename__ = "incorrect_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    user_answer = Column(String(500), nullable=False)
    attempted_at = Column(DateTime, server_default=func.now())
    hint_requested = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User")

class WelcomeEmailSeries(Base):
    """Welcome email series configuration"""
    __tablename__ = "welcome_email_series"
    
    id = Column(Integer, primary_key=True, index=True)
    sequence_number = Column(Integer, nullable=False)
    template_name = Column(String(255), nullable=False)
    subject_line = Column(String(500), nullable=False)
    send_delay_hours = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
