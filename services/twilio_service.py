from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from app.core.config import settings
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    async def send_cryptic_message(self, phone: str, message_data: dict) -> bool:
        """Send tri-weekly cryptic message via SMS (Sun/Wed/Fri)"""
        try:
            # Format message based on day
            day_emoji = self._get_day_emoji(message_data['day_of_week'])
            formatted_message = self._format_triweekly_message(message_data, day_emoji)
            
            message_instance = self.client.messages.create(
                body=formatted_message,
                from_=self.from_number,
                to=phone
            )
            
            logger.info(f"SMS sent successfully to {phone}, Week {message_data['week_number']} {message_data['day_of_week']}, SID: {message_instance.sid}")
            return True
            
        except TwilioException as e:
            logger.error(f"Failed to send SMS to {phone}: {str(e)}")
            return False
    
    async def send_solution_confirmation(self, phone: str, week_number: int, day_of_week: str, is_weekly_complete: bool = False) -> bool:
        """Send confirmation when user solves puzzle"""
        try:
            if is_weekly_complete:
                message = f"🎉 Amazing! You completed ALL 3 puzzles for Week {week_number}! Ready for next week's challenge?"
            else:
                next_day = self._get_next_day(day_of_week)
                message = f"✅ Correct! Week {week_number} {day_of_week} solved! Next challenge: {next_day}"
            
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            return True
            
        except TwilioException as e:
            logger.error(f"Failed to send confirmation SMS to {phone}: {str(e)}")
            return False
    
    async def send_weekly_reminder(self, phone: str, week_number: int, missed_days: list) -> bool:
        """Send reminder for missed messages in the week"""
        try:
            if len(missed_days) == 1:
                message = f"⏰ Don't forget! Week {week_number} {missed_days[0]} puzzle is waiting for you!"
            else:
                days_str = ", ".join(missed_days)
                message = f"⏰ Week {week_number} reminder: You still have {days_str} puzzles to solve!"
            
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            return True
            
        except TwilioException as e:
            logger.error(f"Failed to send reminder SMS to {phone}: {str(e)}")
            return False
    
    def _format_triweekly_message(self, message_data: dict, day_emoji: str) -> str:
        """Format message for tri-weekly delivery (Sun/Wed/Fri)"""
        return f"""{day_emoji} {message_data['title']}

{message_data['message']}

💡 Hint: {message_data.get('hint', 'Think carefully...')}
🏆 Points: {message_data.get('reward_points', 10)}
📅 Week {message_data['week_number']} • {message_data['day_of_week']} Challenge

Reply with your solution or visit our app to submit.
Need a hint? Reply 'HINT' """

    def _format_message(self, message: str, week_number: int, day_of_week: str, message_sequence: int, day_emoji: str) -> str:
        """Legacy format method - keeping for backwards compatibility"""
        return f"""{day_emoji} Week {week_number} - {day_of_week} Challenge

{message}

Reply with your solution or visit our app to submit.
Need a hint? Reply 'HINT' """
    
    def _get_day_emoji(self, day_of_week: str) -> str:
        """Get emoji for each day"""
        emojis = {
            'Sunday': '🌅',
            'Wednesday': '🔥', 
            'Friday': '🎯'
        }
        return emojis.get(day_of_week, '🧩')
    
    def _get_next_day(self, current_day: str) -> str:
        """Get next puzzle day"""
        next_days = {
            'Sunday': 'Wednesday',
            'Wednesday': 'Friday',
            'Friday': 'Next Sunday'
        }
        return next_days.get(current_day, 'Next puzzle')
    
    async def send_subscription_welcome(self, phone: str) -> bool:
        """Send welcome message to new SMS subscribers"""
        try:
            message = """🎉 Welcome to Cryptic Messages!

You'll receive 3 challenges per week:
🌅 Sunday - Week opener
🔥 Wednesday - Mid-week challenge  
🎯 Friday - Week closer

Your first puzzle arrives this Sunday! Get ready to exercise your mind! 🧠"""
            
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            return True
            
        except TwilioException as e:
            logger.error(f"Failed to send welcome SMS to {phone}: {str(e)}")
            return False
