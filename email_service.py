"""
Email Service for Cryptic Messages Subscription
Handles welcome emails and trial message delivery using SendGrid
"""

import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine
import logging

# SendGrid imports
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    print("SendGrid not installed. Run: pip install sendgrid")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # SendGrid configuration for Single Sender Verification
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'crypticmessageswithallmighty1@gmail.com')
        self.from_name = os.getenv('FROM_NAME', 'The Riddle Room - Cipher Academy')
        self.reply_to = 'crypticmessageswithallmighty1@gmail.com'
        
        if not self.sendgrid_api_key:
            logger.warning("⚠️ SENDGRID_API_KEY not found - Get it from SendGrid dashboard")
            logger.info("📋 Go to: https://app.sendgrid.com/settings/api_keys")
        
        if SENDGRID_AVAILABLE and self.sendgrid_api_key:
            self.sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            logger.info("✅ SendGrid initialized for Single Sender Verification")
            logger.info("📧 Sending from: crypticmessageswithallmighty1@gmail.com")
        else:
            self.sg = None
            logger.warning("❌ SendGrid not available - check API key and installation")
        
    def send_welcome_email(self, user_email: str, user_name: str = None):
        """Send welcome email to new beta signup"""
        logger.info(f"Sending welcome email to {user_email}")
        
        subject = "🧩 Welcome to The Riddle Room Beta - Your First Challenge This Sunday!"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f4f4f4;">
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">🏛️ The Riddle Room</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px;">by Cipher Academy</p>
            </div>
            
            <div style="padding: 30px; background: white;">
                <h2 style="color: #1e3c72;">Welcome to the Beta, {user_name or 'Fellow Cryptographer'}! 🎉</h2>
                
                <p style="font-size: 16px; line-height: 1.6;">Thank you for joining The Riddle Room beta program! You're now part of an exclusive group who will help shape the future of cryptographic education.</p>
                
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 25px 0; border-left: 5px solid #FFD700;">
                    <h3 style="margin-top: 0; color: #1e3c72;">🗓️ Your Beta Schedule</h3>
                    <ul style="line-height: 1.8;">
                        <li><strong>First Challenge:</strong> This Sunday at 9:00 AM EST</li>
                        <li><strong>Frequency:</strong> 3 challenges per week (Sun/Wed/Fri)</li>
                        <li><strong>Beta Duration:</strong> 4 weeks (12 total challenges)</li>
                        <li><strong>Difficulty:</strong> Beginner to Intermediate</li>
                    </ul>
                </div>
                
                <div style="background: #e8f4fd; padding: 25px; border-radius: 10px; margin: 25px 0;">
                    <h3 style="margin-top: 0; color: #1e3c72;">🔐 What You'll Learn</h3>
                    <p><strong>Week 1:</strong> Caesar Cipher & Basic Substitution<br>
                    <strong>Week 2:</strong> Pattern Recognition & Frequency Analysis<br>
                    <strong>Week 3:</strong> Polyalphabetic Ciphers (Vigenère)<br>
                    <strong>Week 4:</strong> Modern Cryptography Introduction</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <div style="background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; 
                              padding: 20px; border-radius: 10px; display: inline-block;">
                        <h3 style="margin: 0; font-size: 18px;">⏰ REMINDER</h3>
                        <p style="margin: 10px 0 0 0;">First message goes out this Sunday!</p>
                    </div>
                </div>
                
                <p style="color: #666; font-size: 14px; text-align: center; margin-top: 30px;">
                    Questions? Reply to this email or contact support@riddleroom.com<br>
                    Follow us: @CipherAcademy
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_body)
    
    def send_first_challenge(self, user_email: str):
        """Send the first cryptic challenge"""
        logger.info(f"Sending first challenge to {user_email}")
        
        subject = "🧠 Challenge #1: Caesar's Ancient Secret"
        
        html_body = """
        <html>
        <body style="font-family: 'Courier New', monospace; max-width: 600px; margin: 0 auto; background: #1a1a1a; color: #fff;">
            <div style="background: linear-gradient(135deg, #8B4513 0%, #CD853F 100%); padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">🏛️ THE RIDDLE ROOM</h1>
                <p style="margin: 5px 0 0 0;">Week 1 - Challenge 1</p>
            </div>
            
            <div style="padding: 30px; background: #2a2a2a;">
                <h2 style="color: #FFD700; text-align: center;">⚔️ CAESAR'S SECRET MESSAGE ⚔️</h2>
                
                <div style="background: #1a1a1a; padding: 25px; border-radius: 10px; text-align: center; margin: 20px 0; border: 2px solid #8B4513;">
                    <h3 style="color: #CD853F; letter-spacing: 2px;">DECRYPT THIS:</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #FFD700; letter-spacing: 2px; margin: 20px 0; word-break: break-all;">
                        WKLV LV MXVW WKH EHJLQQLQJ
                    </p>
                </div>
                
                <div style="background: #333; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h4 style="color: #FFD700; margin-top: 0;">📜 Historical Context:</h4>
                    <p>Julius Caesar used this cipher to protect military communications. Each letter is shifted by a fixed number of positions in the alphabet.</p>
                </div>
                
                <div style="background: #2d4a22; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #4CAF50;">
                    <h4 style="color: #90EE90; margin-top: 0;">💡 Hint:</h4>
                    <p>Try shifting each letter back by 3 positions. A→X, B→Y, C→Z, D→A, E→B...</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="mailto:challenges@riddleroom.com?subject=Challenge 1 Answer&body=My answer: " 
                       style="background: #FFD700; color: #1a1a1a; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; font-weight: bold; display: inline-block;">
                        📧 Submit Your Answer
                    </a>
                </div>
                
                <p style="color: #888; font-size: 14px; text-align: center;">
                    Next challenge arrives Wednesday! Good luck, cryptographer. 🔐
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_body)
    
    def _send_email(self, to_email: str, subject: str, html_body: str):
        """Send email using SendGrid API with Single Sender Verification"""
        if not self.sg:
            logger.error("❌ SendGrid client not initialized. Check SENDGRID_API_KEY.")
            logger.info("💡 Get API key from: https://app.sendgrid.com/settings/api_keys")
            return False
            
        try:
            # Create SendGrid mail object with verified single sender
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_body
            )
            
            # Add reply-to for better user experience
            message.reply_to = self.reply_to
            
            # Send email
            response = self.sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"✅ Cryptic message email sent to {to_email}")
                return True
            else:
                logger.error(f"❌ SendGrid error {response.status_code}")
                if response.status_code == 403:
                    logger.error("🔒 Email not verified! Go to SendGrid → Settings → Sender Authentication")
                    logger.error("📧 Verify: crypticmessageswithallmighty1@gmail.com")
                return False
            
        except Exception as e:
            logger.error(f"❌ Email failed for {to_email}: {str(e)}")
            if "sender identity" in str(e).lower():
                logger.error("🔧 Fix: Verify sender in SendGrid dashboard")
            return False
    
    def send_welcome_to_all_beta_users(self):
        """Send welcome emails to all beta trial users who haven't received one yet"""
        logger.info("Sending welcome emails to all beta users")
        
        with engine.connect() as conn:
            # Get all beta users who signed up recently
            result = conn.execute(text("""
                SELECT id, email, experience 
                FROM users 
                WHERE subscription_type = 'beta_trial' 
                AND created_at >= CURRENT_DATE - INTERVAL '7 days'
                ORDER BY created_at DESC
            """))
            
            users = result.fetchall()
            sent_count = 0
            
            for user in users:
                user_id, email, experience = user
                success = self.send_welcome_email(email, experience)
                if success:
                    sent_count += 1
                    
                    # Log the email sent in database (optional)
                    conn.execute(text("""
                        INSERT INTO user_welcome_emails (user_id, template_id, scheduled_at, sent_at, status)
                        VALUES (:user_id, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'sent')
                        ON CONFLICT DO NOTHING
                    """), {"user_id": user_id})
            
            conn.commit()
            logger.info(f"Welcome emails sent to {sent_count} beta users")
            return sent_count

# Initialize the service
email_service = EmailService()
