"""
Automated Scheduling Service for Cryptic Messages
Handles tri-weekly delivery: Sunday 8:00 AM, Wednesday 6:00 PM, Friday 3:00 PM
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from dataclasses import dataclass
import json

from sqlalchemy import create_engine, text
from twilio_service import TwilioService
from sendgrid_service import SendGridService
from welcome_email_service import WelcomeEmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MessageDelivery:
    user_id: int
    phone_number: str
    email: str
    week_number: int
    day_of_week: str
    message_sequence: int
    title: str
    message: str
    difficulty_level: int
    requires_previous_code: bool
    previous_solution: str = None

class CrypticMessageScheduler:
    def __init__(self):
        self.db_engine = create_engine(
            "postgresql://m:Prindle#$%10@localhost/theriddleroom"
        )
        self.twilio = TwilioService()
        self.sendgrid = SendGridService()
        self.welcome_email_service = WelcomeEmailService(self.db_engine, self.sendgrid)
        self.delivery_schedule = {
            'Sunday': '08:00',    # 8:00 AM
            'Wednesday': '18:00', # 6:00 PM  
            'Friday': '15:00'     # 3:00 PM
        }
        
    async def get_active_subscribers(self) -> List[Dict[str, Any]]:
        """Get all users with active subscriptions"""
        query = """
        SELECT DISTINCT 
            u.id as user_id,
            u.phone_number,
            u.email,
            up.current_week,
            u.subscription_status,
            u.subscription_start_date,
            u.subscription_end_date
        FROM users u
        JOIN user_progress up ON u.id = up.user_id
        WHERE u.subscription_status = 'active'
        AND u.subscription_end_date > CURRENT_DATE
        AND u.phone_number IS NOT NULL
        AND u.email IS NOT NULL
        """
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row._mapping) for row in result]

    async def get_message_for_delivery(self, week_number: int, day_of_week: str) -> Dict[str, Any]:
        """Get the specific message for a given week and day"""
        query = """
        SELECT 
            week_number,
            day_of_week,
            message_sequence,
            title,
            message,
            solution_code,
            hint,
            difficulty_level,
            requires_previous_code,
            previous_message_solution
        FROM cryptic_messages
        WHERE week_number = :week_number 
        AND day_of_week = :day_of_week
        AND is_active = true
        """
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query), {
                'week_number': week_number,
                'day_of_week': day_of_week
            })
            row = result.first()
            return dict(row._mapping) if row else None

    async def check_user_eligibility(self, user_id: int, week_number: int, day_of_week: str) -> bool:
        """Check if user has solved previous required challenges"""
        query = """
        SELECT cm.requires_previous_code, cm.previous_message_solution
        FROM cryptic_messages cm
        WHERE cm.week_number = :week_number 
        AND cm.day_of_week = :day_of_week
        """
        
        with self.db_engine.connect() as conn:
            result = conn.execute(text(query), {
                'week_number': week_number,
                'day_of_week': day_of_week
            })
            message_info = result.first()
            
            if not message_info or not message_info.requires_previous_code:
                return True
                
            # Check if user solved the required previous challenge
            prev_query = """
            SELECT COUNT(*) as solved_count
            FROM user_submissions us
            WHERE us.user_id = :user_id
            AND us.is_correct = true
            AND us.submitted_code = :required_solution
            """
            
            prev_result = conn.execute(text(prev_query), {
                'user_id': user_id,
                'required_solution': message_info.previous_message_solution
            })
            
            return prev_result.first().solved_count > 0

    async def send_message_to_user(self, delivery: MessageDelivery) -> bool:
        """Send message via both SMS and Email"""
        success = True
        
        try:
            # Format message for SMS (shorter version)
            sms_message = f"""🔐 CIPHER ACADEMY - Week {delivery.week_number} {delivery.day_of_week}

{delivery.title}

{delivery.message[:200]}{'...' if len(delivery.message) > 200 else ''}

Difficulty: {'⭐' * delivery.difficulty_level}
Reply with your solution code.

Full message: cipher-academy.com/week{delivery.week_number}"""

            # Send SMS
            sms_success = await self.twilio.send_sms(
                to_number=delivery.phone_number,
                message=sms_message
            )
            
            # Format message for Email (full version)
            email_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; text-align: center;">
                    <h1>🔐 The Cipher Academy Journey</h1>
                    <h2>Week {delivery.week_number} • {delivery.day_of_week}</h2>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <h2 style="color: #1e3c72; border-bottom: 2px solid #2a5298; padding-bottom: 10px;">
                        {delivery.title}
                    </h2>
                    
                    <div style="background: white; padding: 20px; border-left: 4px solid #2a5298; margin: 20px 0;">
                        <p style="font-size: 16px; line-height: 1.6; color: #333;">
                            {delivery.message}
                        </p>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin: 20px 0;">
                        <div style="background: #e9ecef; padding: 15px; border-radius: 8px; flex: 1; margin-right: 10px;">
                            <strong>Difficulty Level:</strong><br>
                            {'⭐' * delivery.difficulty_level} ({delivery.difficulty_level}/20)
                        </div>
                        <div style="background: #e9ecef; padding: 15px; border-radius: 8px; flex: 1; margin-left: 10px;">
                            <strong>Challenge Type:</strong><br>
                            {'Requires Previous Code' if delivery.requires_previous_code else 'Standalone Challenge'}
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://cipher-academy.com/submit/{delivery.week_number}/{delivery.day_of_week.lower()}" 
                           style="background: #2a5298; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Submit Your Solution
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #dee2e6; padding-top: 20px; font-size: 14px; color: #6c757d;">
                        <p>Need a hint? Reply to this email or visit your dashboard.</p>
                        <p>Track your progress: <a href="https://cipher-academy.com/progress">cipher-academy.com/progress</a></p>
                    </div>
                </div>
            </div>
            """
            
            # Send Email
            email_success = await self.sendgrid.send_email(
                to_email=delivery.email,
                subject=f"🔐 Week {delivery.week_number} {delivery.day_of_week}: {delivery.title}",
                html_content=email_html,
                from_name="The Cipher Academy"
            )
            
            success = sms_success and email_success
            
            # Log delivery
            if success:
                logger.info(f"Successfully delivered Week {delivery.week_number} {delivery.day_of_week} to user {delivery.user_id}")
            else:
                logger.error(f"Failed to deliver Week {delivery.week_number} {delivery.day_of_week} to user {delivery.user_id}")
                
        except Exception as e:
            logger.error(f"Error sending message to user {delivery.user_id}: {str(e)}")
            success = False
            
        return success

    async def process_scheduled_delivery(self, day_of_week: str):
        """Process all deliveries for a specific day"""
        logger.info(f"Starting {day_of_week} delivery process")
        
        try:
            # Get all active subscribers
            subscribers = await self.get_active_subscribers()
            logger.info(f"Found {len(subscribers)} active subscribers")
            
            delivery_count = 0
            
            for subscriber in subscribers:
                try:
                    # Check user eligibility for current week/day
                    eligible = await self.check_user_eligibility(
                        subscriber['user_id'],
                        subscriber['current_week'],
                        day_of_week
                    )
                    
                    if not eligible:
                        logger.info(f"User {subscriber['user_id']} not eligible for Week {subscriber['current_week']} {day_of_week} - missing previous solution")
                        continue
                    
                    # Get the message for this week/day
                    message_data = await self.get_message_for_delivery(
                        subscriber['current_week'],
                        day_of_week
                    )
                    
                    if not message_data:
                        logger.warning(f"No message found for Week {subscriber['current_week']} {day_of_week}")
                        continue
                    
                    # Create delivery object
                    delivery = MessageDelivery(
                        user_id=subscriber['user_id'],
                        phone_number=subscriber['phone_number'],
                        email=subscriber['email'],
                        week_number=subscriber['current_week'],
                        day_of_week=day_of_week,
                        message_sequence=message_data['message_sequence'],
                        title=message_data['title'],
                        message=message_data['message'],
                        difficulty_level=message_data['difficulty_level'],
                        requires_previous_code=message_data['requires_previous_code'],
                        previous_solution=message_data.get('previous_message_solution')
                    )
                    
                    # Send the message
                    success = await self.send_message_to_user(delivery)
                    
                    if success:
                        delivery_count += 1
                        
                        # Record delivery in database
                        await self.record_delivery(delivery)
                        
                except Exception as e:
                    logger.error(f"Error processing delivery for user {subscriber['user_id']}: {str(e)}")
                    continue
            
            logger.info(f"Completed {day_of_week} delivery: {delivery_count} messages sent")
            
        except Exception as e:
            logger.error(f"Error in {day_of_week} delivery process: {str(e)}")

    async def record_delivery(self, delivery: MessageDelivery):
        """Record successful delivery in database"""
        query = """
        INSERT INTO message_deliveries (
            user_id, week_number, day_of_week, message_sequence,
            delivered_at, delivery_method
        ) VALUES (
            :user_id, :week_number, :day_of_week, :message_sequence,
            CURRENT_TIMESTAMP, 'sms_email'
        )
        ON CONFLICT (user_id, week_number, day_of_week) 
        DO UPDATE SET delivered_at = CURRENT_TIMESTAMP
        """
        
        try:
            with self.db_engine.connect() as conn:
                conn.execute(text(query), {
                    'user_id': delivery.user_id,
                    'week_number': delivery.week_number,
                    'day_of_week': delivery.day_of_week,
                    'message_sequence': delivery.message_sequence
                })
                conn.commit()
        except Exception as e:
            logger.error(f"Error recording delivery: {str(e)}")

    def setup_schedule(self):
        """Setup the delivery schedule"""
        # Sunday 8:00 AM
        schedule.every().sunday.at("08:00").do(
            lambda: asyncio.run(self.process_delivery('Sunday'))
        )
        
        # Wednesday 6:00 PM  
        schedule.every().wednesday.at("18:00").do(
            lambda: asyncio.run(self.process_delivery('Wednesday'))
        )
        
        # Friday 3:00 PM
        schedule.every().friday.at("15:00").do(
            lambda: asyncio.run(self.process_delivery('Friday'))
        )
        
        # Process welcome emails every 15 minutes
        schedule.every(15).minutes.do(
            lambda: asyncio.run(self.process_welcome_emails())
        )
        
        logger.info("Delivery schedule configured: Sunday 8AM, Wednesday 6PM, Friday 3PM")
        logger.info("Welcome email processing: Every 15 minutes")

    async def process_welcome_emails(self):
        """Process pending welcome emails"""
        try:
            sent_count = await self.welcome_email_service.process_pending_welcome_emails()
            if sent_count > 0:
                logger.info(f"Processed {sent_count} welcome emails")
        except Exception as e:
            logger.error(f"Error processing welcome emails: {str(e)}")

    def run_scheduler(self):
        """Run the scheduling service"""
        logger.info("Starting Cryptic Message Scheduler Service...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(300)  # Wait 5 minutes before retrying

    def run_scheduler(self):
        """Run the scheduling service"""
        logger.info("Starting Cryptic Message Scheduler Service...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(300)  # Wait 5 minutes before retrying

    async def send_test_message(self, user_id: int, week_number: int, day_of_week: str):
        """Send a test message for debugging"""
        logger.info(f"Sending test message: Week {week_number} {day_of_week} to user {user_id}")
        
        subscribers = await self.get_active_subscribers()
        subscriber = next((s for s in subscribers if s['user_id'] == user_id), None)
        
        if not subscriber:
            logger.error(f"User {user_id} not found or not active")
            return False
            
        message_data = await self.get_message_for_delivery(week_number, day_of_week)
        
        if not message_data:
            logger.error(f"No message found for Week {week_number} {day_of_week}")
            return False
            
        delivery = MessageDelivery(
            user_id=subscriber['user_id'],
            phone_number=subscriber['phone_number'],
            email=subscriber['email'],
            week_number=week_number,
            day_of_week=day_of_week,
            message_sequence=message_data['message_sequence'],
            title=message_data['title'],
            message=message_data['message'],
            difficulty_level=message_data['difficulty_level'],
            requires_previous_code=message_data['requires_previous_code'],
            previous_solution=message_data.get('previous_message_solution')
        )
        
        return await self.send_message_to_user(delivery)

if __name__ == "__main__":
    scheduler = CrypticMessageScheduler()
    scheduler.setup_schedule()
    scheduler.run_scheduler()
