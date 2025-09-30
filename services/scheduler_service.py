from services.twilio_service import TwilioService
from services.sendgrid_service import SendGridService
from services.stripe_service import StripeService
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class MessageSchedulerService:
    """Handles tri-weekly message scheduling and delivery"""
    
    def __init__(self):
        self.twilio = TwilioService()
        self.sendgrid = SendGridService()
        self.stripe = StripeService()
    
    async def send_weekly_messages(self, week_number: int, day_of_week: str):
        """Send cryptic messages to all active subscribers for specific day"""
        try:
            # Get message for this week and day
            from app.database import get_db
            from app.models.cryptic_message import CrypticMessage
            from app.models.user import User
            
            db = next(get_db())
            
            # Get the message for this week and day
            message = db.query(CrypticMessage).filter(
                CrypticMessage.week_number == week_number,
                CrypticMessage.day_of_week == day_of_week,
                CrypticMessage.is_active == True
            ).first()
            
            if not message:
                logger.error(f"No message found for Week {week_number} {day_of_week}")
                return
            
            # Get all active subscribers
            active_users = db.query(User).filter(
                User.is_active == True,
                User.subscription_id != None
            ).all()
            
            logger.info(f"Sending Week {week_number} {day_of_week} messages to {len(active_users)} subscribers")
            
            # Send messages concurrently
            tasks = []
            for user in active_users:
                tasks.append(self._send_user_message(user, message))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log results
            successful = sum(1 for r in results if r is True)
            failed = len(results) - successful
            
            logger.info(f"Message delivery complete: {successful} successful, {failed} failed")
            
        except Exception as e:
            logger.error(f"Error in weekly message delivery: {str(e)}")
    
    async def _send_user_message(self, user, message) -> bool:
        """Send message to individual user via both SMS and email"""
        try:
            # Check if user should receive this message based on their progress
            if not await self._should_user_receive_message(user, message):
                return True  # Skip but don't count as failure
            
            tasks = []
            
            # Send email (always send)
            tasks.append(
                self.sendgrid.send_cryptic_email(
                    user.email,
                    message.message,
                    message.week_number,
                    message.day_of_week,
                    message.message_sequence,
                    message.hint
                )
            )
            
            # Send SMS if user has phone number
            if user.phone:
                tasks.append(
                    self.twilio.send_cryptic_message(
                        user.phone,
                        message.message,
                        message.week_number,
                        message.day_of_week,
                        message.message_sequence
                    )
                )
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log message delivery in database
            await self._log_message_delivery(user.id, message)
            
            return all(r is True for r in results if not isinstance(r, Exception))
            
        except Exception as e:
            logger.error(f"Failed to send message to user {user.email}: {str(e)}")
            return False
    
    async def _should_user_receive_message(self, user, message) -> bool:
        """Check if user should receive this message based on their progress"""
        from app.database import get_db
        from app.models.user_progress import UserProgress
        
        db = next(get_db())
        progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
        
        if not progress:
            # New user, should receive week 1 messages
            return message.week_number == 1
        
        # User should receive messages for their current week or if they're caught up
        return message.week_number <= progress.current_week + 1
    
    async def _log_message_delivery(self, user_id: int, message):
        """Log that a message was delivered to user"""
        try:
            from app.database import get_db
            from app.models.message_delivery import MessageDelivery
            
            db = next(get_db())
            
            delivery_log = MessageDelivery(
                user_id=user_id,
                message_id=message.id,
                week_number=message.week_number,
                day_of_week=message.day_of_week,
                delivered_at=datetime.utcnow()
            )
            
            db.add(delivery_log)
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to log message delivery: {str(e)}")
    
    async def send_weekly_reminders(self, week_number: int):
        """Send reminders for users who missed messages this week"""
        try:
            from app.database import get_db
            from app.models.user import User
            from app.models.user_submissions import UserSubmission
            
            db = next(get_db())
            
            # Get all active users
            active_users = db.query(User).filter(
                User.is_active == True,
                User.subscription_id != None
            ).all()
            
            for user in active_users:
                # Check which days they missed this week
                submitted_days = db.query(UserSubmission.day_of_week).filter(
                    UserSubmission.user_id == user.id,
                    UserSubmission.week_number == week_number,
                    UserSubmission.is_correct == True
                ).all()
                
                submitted_days = [day[0] for day in submitted_days]
                all_days = ['Sunday', 'Wednesday', 'Friday']
                missed_days = [day for day in all_days if day not in submitted_days]
                
                if missed_days:
                    # Send reminder via SMS if available
                    if user.phone:
                        await self.twilio.send_weekly_reminder(user.phone, week_number, missed_days)
                    
                    # Send reminder email
                    await self.sendgrid.send_weekly_summary_email(
                        user.email, week_number, submitted_days, missed_days
                    )
            
        except Exception as e:
            logger.error(f"Error sending weekly reminders: {str(e)}")
    
    async def handle_correct_submission(self, user_id: int, week_number: int, day_of_week: str, solution: str):
        """Handle when user submits correct solution"""
        try:
            from app.database import get_db
            from app.models.user import User
            from app.models.user_submissions import UserSubmission
            from app.models.user_progress import UserProgress
            
            db = next(get_db())
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return
            
            # Check if this completes the week (all 3 puzzles solved)
            week_submissions = db.query(UserSubmission).filter(
                UserSubmission.user_id == user_id,
                UserSubmission.week_number == week_number,
                UserSubmission.is_correct == True
            ).count()
            
            is_weekly_complete = week_submissions >= 3
            
            # Send confirmation messages
            if user.phone:
                await self.twilio.send_solution_confirmation(
                    user.phone, week_number, day_of_week, is_weekly_complete
                )
            
            await self.sendgrid.send_solution_confirmation_email(
                user.email, week_number, day_of_week, solution, is_weekly_complete
            )
            
            # Update user progress if week is complete
            if is_weekly_complete:
                progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
                if progress:
                    progress.current_week = max(progress.current_week, week_number + 1)
                    progress.total_solved += 1
                    progress.current_streak += 1
                    progress.longest_streak = max(progress.longest_streak, progress.current_streak)
                    progress.last_solved_at = datetime.utcnow()
                    db.commit()
            
        except Exception as e:
            logger.error(f"Error handling correct submission: {str(e)}")
    
    def get_next_delivery_times(self) -> Dict[str, datetime]:
        """Get next scheduled delivery times for each day"""
        now = datetime.utcnow()
        current_week = now.isocalendar()[1]
        
        # Calculate next Sunday, Wednesday, Friday
        days_ahead = {
            'Sunday': (6 - now.weekday()) % 7,
            'Wednesday': (2 - now.weekday()) % 7,
            'Friday': (4 - now.weekday()) % 7
        }
        
        next_times = {}
        for day, days_ahead in days_ahead.items():
            if days_ahead == 0:  # Today
                next_date = now.replace(hour=9, minute=0, second=0, microsecond=0)
                if next_date <= now:  # Already passed today
                    next_date += timedelta(days=7)
            else:
                next_date = now + timedelta(days=days_ahead)
                next_date = next_date.replace(hour=9, minute=0, second=0, microsecond=0)
            
            next_times[day] = next_date
        
        return next_times
