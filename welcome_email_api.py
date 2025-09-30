"""
Welcome Email API Endpoints
FastAPI routes for managing welcome email series
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from sqlalchemy import create_engine, text
from welcome_email_service import WelcomeEmailService

logger = logging.getLogger(__name__)

# Database connection
db_engine = create_engine("postgresql://m:Prindle#$%10@localhost/theriddleroom")

# Router for welcome email endpoints
welcome_router = APIRouter(prefix="/api/welcome-emails", tags=["Welcome Emails"])

# Pydantic models
class ChallengeSubmission(BaseModel):
    user_id: int
    email_sequence: int
    challenge_type: str
    solution: str

class EmailEventWebhook(BaseModel):
    email: str
    event: str
    timestamp: Optional[datetime] = None
    sg_message_id: str

class WelcomeEmailStats(BaseModel):
    total_emails: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    failed_count: int
    open_rate: float
    click_rate: float

# Dependency to get welcome email service
def get_welcome_service():
    from sendgrid_service import SendGridService
    sendgrid = SendGridService()
    return WelcomeEmailService(db_engine, sendgrid)

@welcome_router.post("/trigger-manual-send")
async def trigger_manual_welcome_emails(background_tasks: BackgroundTasks):
    """Manually trigger welcome email processing (for testing)"""
    try:
        welcome_service = get_welcome_service()
        background_tasks.add_task(welcome_service.process_pending_welcome_emails)
        return {"message": "Welcome email processing triggered"}
    except Exception as e:
        logger.error(f"Error triggering welcome emails: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to trigger welcome emails")

@welcome_router.post("/challenge-submission")
async def submit_challenge_solution(submission: ChallengeSubmission):
    """Handle challenge submissions from welcome emails"""
    try:
        welcome_service = get_welcome_service()
        is_correct = await welcome_service.handle_challenge_submission(
            submission.user_id,
            submission.email_sequence,
            submission.challenge_type,
            submission.solution
        )
        
        if is_correct:
            return {
                "success": True,
                "message": "Correct! Well done on solving the cipher.",
                "is_correct": True
            }
        else:
            return {
                "success": True,
                "message": "Not quite right. Try again! Remember to check the hints in the email.",
                "is_correct": False
            }
    
    except Exception as e:
        logger.error(f"Error processing challenge submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process submission")

@welcome_router.post("/sendgrid-webhook")
async def handle_sendgrid_webhook(events: List[EmailEventWebhook]):
    """Handle SendGrid webhook events for email tracking"""
    try:
        welcome_service = get_welcome_service()
        
        for event in events:
            if event.sg_message_id:
                await welcome_service.track_email_event(
                    event.sg_message_id,
                    event.event,
                    event.timestamp or datetime.now()
                )
        
        return {"message": f"Processed {len(events)} events"}
    
    except Exception as e:
        logger.error(f"Error processing SendGrid webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process webhook")

@welcome_router.get("/stats/{user_id}")
async def get_user_welcome_stats(user_id: int) -> WelcomeEmailStats:
    """Get welcome email statistics for a specific user"""
    try:
        welcome_service = get_welcome_service()
        stats = await welcome_service.get_welcome_email_stats(user_id)
        return WelcomeEmailStats(**stats)
    
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@welcome_router.get("/stats")
async def get_overall_welcome_stats() -> WelcomeEmailStats:
    """Get overall welcome email statistics"""
    try:
        welcome_service = get_welcome_service()
        stats = await welcome_service.get_welcome_email_stats()
        return WelcomeEmailStats(**stats)
    
    except Exception as e:
        logger.error(f"Error getting overall stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@welcome_router.get("/user/{user_id}/progress")
async def get_user_welcome_progress(user_id: int):
    """Get user's progress through welcome email series"""
    try:
        query = """
        SELECT 
            uwe.email_sequence,
            uwe.scheduled_at,
            uwe.sent_at,
            uwe.opened_at,
            uwe.clicked_at,
            uwe.status,
            et.template_name,
            et.subject,
            ecs.submitted_solution,
            ecs.is_correct as challenge_completed
        FROM user_welcome_emails uwe
        JOIN welcome_email_series wes ON wes.email_sequence = uwe.email_sequence
        JOIN email_templates et ON et.id = wes.template_id
        LEFT JOIN email_challenge_submissions ecs ON ecs.user_id = uwe.user_id 
            AND ecs.email_sequence = uwe.email_sequence
        WHERE uwe.user_id = :user_id
        ORDER BY uwe.email_sequence
        """
        
        with db_engine.connect() as conn:
            result = conn.execute(text(query), {"user_id": user_id})
            
            progress = []
            for row in result:
                progress.append({
                    "email_sequence": row.email_sequence,
                    "template_name": row.template_name,
                    "subject": row.subject,
                    "scheduled_at": row.scheduled_at,
                    "sent_at": row.sent_at,
                    "opened_at": row.opened_at,
                    "clicked_at": row.clicked_at,
                    "status": row.status,
                    "challenge_completed": row.challenge_completed,
                    "submitted_solution": row.submitted_solution
                })
            
            return {"user_id": user_id, "welcome_progress": progress}
    
    except Exception as e:
        logger.error(f"Error getting user progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user progress")

@welcome_router.post("/resend/{user_id}/{email_sequence}")
async def resend_welcome_email(user_id: int, email_sequence: int, background_tasks: BackgroundTasks):
    """Resend a specific welcome email to a user"""
    try:
        # Reset email status to scheduled
        query = """
        UPDATE user_welcome_emails 
        SET status = 'scheduled', 
            scheduled_at = CURRENT_TIMESTAMP,
            sent_at = NULL,
            error_message = NULL
        WHERE user_id = :user_id AND email_sequence = :email_sequence
        """
        
        with db_engine.connect() as conn:
            result = conn.execute(text(query), {
                "user_id": user_id,
                "email_sequence": email_sequence
            })
            conn.commit()
            
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Welcome email not found")
        
        # Trigger processing
        welcome_service = get_welcome_service()
        background_tasks.add_task(welcome_service.process_pending_welcome_emails)
        
        return {"message": f"Welcome email {email_sequence} rescheduled for user {user_id}"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resending welcome email: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to resend email")

@welcome_router.put("/preferences/{user_id}")
async def update_email_preferences(user_id: int, preferences: Dict[str, bool]):
    """Update user's email preferences"""
    try:
        # Validate preference keys
        valid_keys = {
            'welcome_series_enabled',
            'marketing_emails_enabled', 
            'challenge_emails_enabled',
            'community_emails_enabled'
        }
        
        invalid_keys = set(preferences.keys()) - valid_keys
        if invalid_keys:
            raise HTTPException(status_code=400, detail=f"Invalid preference keys: {invalid_keys}")
        
        # Build update query
        set_clauses = []
        params = {"user_id": user_id}
        
        for key, value in preferences.items():
            set_clauses.append(f"{key} = :{key}")
            params[key] = value
        
        query = f"""
        UPDATE user_email_preferences 
        SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = :user_id
        """
        
        with db_engine.connect() as conn:
            result = conn.execute(text(query), params)
            conn.commit()
            
            if result.rowcount == 0:
                # Insert new preferences if none exist
                insert_query = """
                INSERT INTO user_email_preferences (user_id, welcome_series_enabled, 
                    marketing_emails_enabled, challenge_emails_enabled, community_emails_enabled)
                VALUES (:user_id, :welcome_series_enabled, :marketing_emails_enabled, 
                    :challenge_emails_enabled, :community_emails_enabled)
                """
                conn.execute(text(insert_query), {
                    "user_id": user_id,
                    "welcome_series_enabled": preferences.get('welcome_series_enabled', True),
                    "marketing_emails_enabled": preferences.get('marketing_emails_enabled', True),
                    "challenge_emails_enabled": preferences.get('challenge_emails_enabled', True),
                    "community_emails_enabled": preferences.get('community_emails_enabled', True)
                })
                conn.commit()
        
        return {"message": "Email preferences updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating email preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

@welcome_router.get("/templates")
async def get_email_templates():
    """Get all email templates"""
    try:
        query = """
        SELECT 
            et.id,
            et.template_name,
            et.subject,
            et.template_variables,
            wes.email_sequence,
            wes.delay_hours,
            wes.is_active
        FROM email_templates et
        JOIN welcome_email_series wes ON wes.template_id = et.id
        ORDER BY wes.email_sequence
        """
        
        with db_engine.connect() as conn:
            result = conn.execute(text(query))
            
            templates = []
            for row in result:
                templates.append({
                    "id": row.id,
                    "template_name": row.template_name,
                    "subject": row.subject,
                    "email_sequence": row.email_sequence,
                    "delay_hours": row.delay_hours,
                    "is_active": row.is_active,
                    "template_variables": row.template_variables
                })
            
            return {"templates": templates}
    
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get templates")
