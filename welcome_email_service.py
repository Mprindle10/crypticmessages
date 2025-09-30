"""
Welcome Email Series Service
Handles automated delivery of 7-email onboarding sequence
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class WelcomeEmailData:
    user_id: int
    email: str
    email_sequence: int
    template_name: str
    subject: str
    html_content: str
    plain_text_content: str
    template_variables: Dict[str, Any]
    scheduled_id: int

class WelcomeEmailService:
    def __init__(self, db_engine: Engine, sendgrid_service):
        self.db_engine = db_engine
        self.sendgrid = sendgrid_service
        
    async def process_pending_welcome_emails(self) -> int:
        """Process all pending welcome emails and send them"""
        try:
            pending_emails = await self.get_pending_welcome_emails()
            sent_count = 0
            
            for email_data in pending_emails:
                try:
                    # Personalize email content
                    personalized_content = await self.personalize_email_content(email_data)
                    
                    # Send email via SendGrid
                    message_id = await self.send_welcome_email(
                        email_data.email,
                        personalized_content['subject'],
                        personalized_content['html_content'],
                        personalized_content['plain_text_content']
                    )
                    
                    # Mark as sent in database
                    await self.mark_email_sent(email_data.scheduled_id, message_id)
                    sent_count += 1
                    
                    logger.info(f"Sent welcome email {email_data.email_sequence} to {email_data.email}")
                    
                except Exception as e:
                    logger.error(f"Failed to send welcome email {email_data.email_sequence} to {email_data.email}: {str(e)}")
                    await self.mark_email_failed(email_data.scheduled_id, str(e))
            
            return sent_count
            
        except Exception as e:
            logger.error(f"Error processing welcome emails: {str(e)}")
            return 0
    
    async def get_pending_welcome_emails(self) -> List[WelcomeEmailData]:
        """Get all pending welcome emails from database"""
        query = "SELECT * FROM get_pending_welcome_emails();"
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query))
            emails = []
            
            for row in result:
                emails.append(WelcomeEmailData(
                    user_id=row.user_id,
                    email=row.email,
                    email_sequence=row.email_sequence,
                    template_name=row.template_name,
                    subject=row.subject,
                    html_content=row.html_content,
                    plain_text_content=row.plain_text_content,
                    template_variables=row.template_variables or {},
                    scheduled_id=row.scheduled_id
                ))
            
            return emails
    
    async def personalize_email_content(self, email_data: WelcomeEmailData) -> Dict[str, str]:
        """Personalize email content with user-specific data"""
        try:
            # Get user data for personalization
            user_data = await self.get_user_personalization_data(email_data.user_id)
            
            # Merge template variables with user data
            variables = {
                **email_data.template_variables,
                **user_data,
                'user_email': email_data.email,
                'email_sequence': email_data.email_sequence
            }
            
            # Replace placeholders in content
            personalized_html = self.replace_template_variables(email_data.html_content, variables)
            personalized_text = self.replace_template_variables(email_data.plain_text_content, variables)
            personalized_subject = self.replace_template_variables(email_data.subject, variables)
            
            return {
                'subject': personalized_subject,
                'html_content': personalized_html,
                'plain_text_content': personalized_text
            }
            
        except Exception as e:
            logger.error(f"Error personalizing email content: {str(e)}")
            # Return original content if personalization fails
            return {
                'subject': email_data.subject,
                'html_content': email_data.html_content,
                'plain_text_content': email_data.plain_text_content
            }
    
    async def get_user_personalization_data(self, user_id: int) -> Dict[str, Any]:
        """Get user-specific data for email personalization"""
        query = """
        SELECT 
            u.email,
            u.created_at,
            COALESCE(up.weeks_completed, 0) as weeks_completed,
            COALESCE(up.current_level, 1) as current_level,
            COALESCE(up.current_era, 'Ancient Foundations') as current_era,
            COALESCE(up.total_correct_answers, 0) as total_correct,
            COALESCE(up.total_attempts, 0) as total_attempts
        FROM users u
        LEFT JOIN user_progress up ON up.user_id = u.id
        WHERE u.id = :user_id
        """
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query), {"user_id": user_id}).fetchone()
            
            if result:
                # Calculate accuracy rate
                accuracy = 0
                if result.total_attempts > 0:
                    accuracy = round((result.total_correct / result.total_attempts) * 100)
                
                # Calculate days since signup
                days_since_signup = (datetime.now() - result.created_at).days
                
                return {
                    'user_name': result.email.split('@')[0].title(),  # Use email prefix as name
                    'weeks_completed': result.weeks_completed,
                    'current_level': result.current_level,
                    'current_era': result.current_era,
                    'accuracy_rate': accuracy,
                    'days_since_signup': days_since_signup,
                    'dashboard_url': f"https://cipher-academy.com/dashboard?user={user_id}",
                    'community_url': "https://cipher-academy.com/community",
                    'discord_url': "https://cipher-academy.com/discord",
                    'practice_url': "https://cipher-academy.com/practice",
                    'upgrade_url': f"https://cipher-academy.com/upgrade?user={user_id}",
                    'preview_url': "https://cipher-academy.com/preview-industrial"
                }
            
            return {
                'user_name': 'Fellow Cryptographer',
                'weeks_completed': 0,
                'current_level': 1,
                'current_era': 'Ancient Foundations',
                'accuracy_rate': 0
            }
    
    def replace_template_variables(self, content: str, variables: Dict[str, Any]) -> str:
        """Replace template variables in content"""
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    async def send_welcome_email(self, to_email: str, subject: str, html_content: str, text_content: str) -> str:
        """Send welcome email via SendGrid"""
        try:
            # Add personalization for current challenges
            if "XIBKGZIVNVMG" in html_content:  # Atbash challenge
                html_content = html_content.replace("XIBKGZIVNVMG", "XIBKGZIVNVMG")  # Already correct
            
            if "ZHOFRPH WR WKH FLSKHU DFDGHPB" in html_content:  # Caesar challenge
                html_content = html_content.replace("ZHOFRPH WR WKH FLSKHU DFDGHPB", "ZHOFRPH WR WKH FLSKHU DFDGHPB")
            
            # Add current community challenge
            current_challenge = await self.get_current_community_challenge()
            html_content = html_content.replace("{weekly_challenge}", current_challenge)
            
            # Send via SendGrid
            message_id = await self.sendgrid.send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email="academy@cipher-academy.com",
                from_name="The Cipher Academy"
            )
            
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise
    
    async def get_current_community_challenge(self) -> str:
        """Get current community challenge for email insertion"""
        # This could be dynamically generated or pulled from database
        challenges = [
            "13 34 32 32 45 33 24 44 54",  # Polybius Square
            "WKLV LV D FDVWDU FLSKHU",     # Caesar Cipher
            "XIBKGZIVNVMG",                # Atbash Cipher
            "16-5-5-11 2-5-8-9-14-4 20-8-5 22-5-9-12"  # A1Z26
        ]
        
        # Rotate based on current week
        week_num = datetime.now().isocalendar()[1]
        return challenges[week_num % len(challenges)]
    
    async def mark_email_sent(self, scheduled_id: int, message_id: str):
        """Mark welcome email as sent in database"""
        query = "SELECT mark_welcome_email_sent(:scheduled_id, :message_id)"
        
        with self.db_engine.connect() as conn:
            conn.execute(text(query), {
                "scheduled_id": scheduled_id,
                "message_id": message_id
            })
            conn.commit()
    
    async def mark_email_failed(self, scheduled_id: int, error_message: str):
        """Mark welcome email as failed in database"""
        query = """
        UPDATE user_welcome_emails 
        SET status = 'failed', error_message = :error_message
        WHERE id = :scheduled_id
        """
        
        with self.db_engine.connect() as conn:
            conn.execute(text(query), {
                "scheduled_id": scheduled_id,
                "error_message": error_message
            })
            conn.commit()
    
    async def track_email_event(self, message_id: str, event_type: str, timestamp: datetime = None):
        """Track email events (opens, clicks, etc.)"""
        if timestamp is None:
            timestamp = datetime.now()
        
        query = "SELECT track_welcome_email_event(:message_id, :event_type, :timestamp)"
        
        with self.db_engine.connect() as conn:
            conn.execute(text(query), {
                "message_id": message_id,
                "event_type": event_type,
                "timestamp": timestamp
            })
            conn.commit()
    
    async def handle_challenge_submission(self, user_id: int, email_sequence: int, 
                                        challenge_type: str, solution: str) -> bool:
        """Handle challenge submission from welcome emails"""
        # Validate solution
        is_correct = await self.validate_challenge_solution(challenge_type, solution)
        
        # Store submission
        query = """
        INSERT INTO email_challenge_submissions 
        (user_id, email_sequence, challenge_type, submitted_solution, is_correct)
        VALUES (:user_id, :email_sequence, :challenge_type, :solution, :is_correct)
        ON CONFLICT (user_id, email_sequence) 
        DO UPDATE SET 
            submitted_solution = :solution,
            is_correct = :is_correct,
            submitted_at = CURRENT_TIMESTAMP
        """
        
        with self.db_engine.connect() as conn:
            conn.execute(text(query), {
                "user_id": user_id,
                "email_sequence": email_sequence,
                "challenge_type": challenge_type,
                "solution": solution,
                "is_correct": is_correct
            })
            conn.commit()
        
        return is_correct
    
    async def validate_challenge_solution(self, challenge_type: str, solution: str) -> bool:
        """Validate challenge solutions"""
        solution = solution.upper().strip()
        
        solutions = {
            'caesar': 'WELCOME TO THE CIPHER ACADEMY',
            'atbash': 'CRYPTANALYSIS',
            'polybius': 'COMMUNITY',
            'a1z26': 'PEEK BEHIND THE VEIL'
        }
        
        return solutions.get(challenge_type, '').upper() == solution
    
    async def get_welcome_email_stats(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get welcome email statistics"""
        where_clause = "WHERE uwe.user_id = :user_id" if user_id else ""
        params = {"user_id": user_id} if user_id else {}
        
        query = f"""
        SELECT 
            COUNT(*) as total_emails,
            COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent_count,
            COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count,
            COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END) as opened_count,
            COUNT(CASE WHEN clicked_at IS NOT NULL THEN 1 END) as clicked_count,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count
        FROM user_welcome_emails uwe
        {where_clause}
        """
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query), params).fetchone()
            
            return {
                'total_emails': result.total_emails,
                'sent_count': result.sent_count,
                'delivered_count': result.delivered_count,
                'opened_count': result.opened_count,
                'clicked_count': result.clicked_count,
                'failed_count': result.failed_count,
                'open_rate': round((result.opened_count / max(result.delivered_count, 1)) * 100, 2),
                'click_rate': round((result.clicked_count / max(result.delivered_count, 1)) * 100, 2)
            }

# Integration function for existing scheduler
async def integrate_welcome_emails_to_scheduler(scheduler_service):
    """Integrate welcome email processing into existing scheduler"""
    
    # Add welcome email processing to scheduler
    welcome_service = WelcomeEmailService(
        scheduler_service.db_engine,
        scheduler_service.sendgrid
    )
    
    # Process welcome emails every 15 minutes
    async def process_welcome_emails():
        sent_count = await welcome_service.process_pending_welcome_emails()
        if sent_count > 0:
            logger.info(f"Processed {sent_count} welcome emails")
    
    # Add to scheduler's task list
    scheduler_service.welcome_email_service = welcome_service
    
    return welcome_service
