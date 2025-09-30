from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class SendGridService:
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = settings.FROM_EMAIL
    
    async def send_cryptic_email(self, email: str, message: str, week_number: int, day_of_week: str, message_sequence: int, hint: str = None) -> bool:
        """Send tri-weekly cryptic message via email"""
        try:
            subject = f"Week {week_number} - {day_of_week} Challenge ({message_sequence}/3)"
            
            mail = Mail(
                from_email=Email(self.from_email, "Cryptic Messages"),
                to_emails=To(email),
                subject=subject,
                html_content=self._format_cryptic_email(message, week_number, day_of_week, message_sequence, hint)
            )
            
            response = self.sg.send(mail)
            logger.info(f"Email sent successfully to {email}, Week {week_number} {day_of_week}, status: {response.status_code}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {str(e)}")
            return False
    
    async def send_solution_confirmation_email(self, email: str, week_number: int, day_of_week: str, solution: str, is_weekly_complete: bool = False) -> bool:
        """Send confirmation email when user solves puzzle"""
        try:
            if is_weekly_complete:
                subject = f"🎉 Week {week_number} Complete! All 3 Puzzles Solved"
                content = self._format_weekly_completion_email(week_number)
            else:
                subject = f"✅ Week {week_number} {day_of_week} - Puzzle Solved!"
                content = self._format_solution_confirmation_email(week_number, day_of_week, solution)
            
            mail = Mail(
                from_email=Email(self.from_email, "Cryptic Messages"),
                to_emails=To(email),
                subject=subject,
                html_content=content
            )
            
            response = self.sg.send(mail)
            return True
            
        except Exception as e:
            logger.error(f"Failed to send confirmation email to {email}: {str(e)}")
            return False
    
    async def send_weekly_summary_email(self, email: str, week_number: int, solved_days: list, missed_days: list) -> bool:
        """Send weekly summary email"""
        try:
            subject = f"Week {week_number} Summary - Your Cryptic Journey"
            
            mail = Mail(
                from_email=Email(self.from_email, "Cryptic Messages"),
                to_emails=To(email),
                subject=subject,
                html_content=self._format_weekly_summary_email(week_number, solved_days, missed_days)
            )
            
            response = self.sg.send(mail)
            return True
            
        except Exception as e:
            logger.error(f"Failed to send weekly summary email to {email}: {str(e)}")
            return False
    
    async def send_welcome_email(self, email: str) -> bool:
        """Send welcome email to new subscribers"""
        try:
            mail = Mail(
                from_email=Email(self.from_email, "Cryptic Messages"),
                to_emails=To(email),
                subject="Welcome to Your 21-Month Cryptic Journey! 🧩",
                html_content=self._format_welcome_email()
            )
            
            response = self.sg.send(mail)
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            return False
    
    def _format_cryptic_email(self, message: str, week_number: int, day_of_week: str, sequence: int, hint: str = None) -> str:
        """Format the cryptic message email"""
        day_colors = {
            'Sunday': '#ff6b6b',    # Red
            'Wednesday': '#4ecdc4', # Teal  
            'Friday': '#45b7d1'     # Blue
        }
        
        day_emojis = {
            'Sunday': '🌅',
            'Wednesday': '🔥',
            'Friday': '🎯'
        }
        
        color = day_colors.get(day_of_week, '#2c3e50')
        emoji = day_emojis.get(day_of_week, '🧩')
        
        hint_section = f"""
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4 style="color: #856404; margin: 0 0 10px 0;">💡 Need a Hint?</h4>
            <p style="margin: 0; color: #856404;">{hint}</p>
        </div>
        """ if hint else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
            <div style="background: {color}; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">{emoji} Week {week_number} - {day_of_week}</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Challenge {sequence} of 3</p>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 0 0 8px 8px;">
                <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0; border-left: 4px solid {color};">
                    <h3 style="color: {color}; margin: 0 0 15px 0;">🔍 Your Cryptic Challenge</h3>
                    <p style="font-size: 16px; line-height: 1.8; color: #2c3e50; margin: 0; font-style: italic;">{message}</p>
                </div>
                
                {hint_section}
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{settings.FRONTEND_URL}/submit" style="background: {color}; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Submit Your Solution</a>
                </div>
                
                <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #2c3e50;"><strong>Remember:</strong> Each puzzle builds on the previous one. Keep your solutions safe!</p>
                </div>
            </div>
            
            <div style="text-align: center; padding: 20px; color: #6c757d; font-size: 12px;">
                <p>Cryptic Messages - Week {week_number} of your 21-month journey</p>
            </div>
        </body>
        </html>
        """
    
    def _format_welcome_email(self) -> str:
        """Format welcome email for new subscribers"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">🎉 Welcome to Cryptic Messages!</h1>
                <p style="margin: 15px 0 0 0; font-size: 18px; opacity: 0.9;">Your 21-month puzzle journey begins now</p>
            </div>
            
            <div style="background: white; padding: 40px 30px; border-radius: 0 0 8px 8px;">
                <h2 style="color: #2c3e50; text-align: center;">🧩 How It Works</h2>
                
                <div style="display: flex; justify-content: space-around; margin: 30px 0;">
                    <div style="text-align: center; flex: 1; margin: 0 10px;">
                        <div style="background: #ff6b6b; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">🌅</div>
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">Sunday</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 14px;">Week opener - Introduction</p>
                    </div>
                    
                    <div style="text-align: center; flex: 1; margin: 0 10px;">
                        <div style="background: #4ecdc4; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">🔥</div>
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">Wednesday</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 14px;">Mid-week challenge</p>
                    </div>
                    
                    <div style="text-align: center; flex: 1; margin: 0 10px;">
                        <div style="background: #45b7d1; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 24px;">🎯</div>
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">Friday</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 14px;">Week closer - Mastery</p>
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 30px 0;">
                    <h3 style="color: #2c3e50; margin: 0 0 15px 0;">📈 Progressive Difficulty</h3>
                    <ul style="color: #6c757d; margin: 0; padding-left: 20px;">
                        <li>Each puzzle builds on previous solutions</li>
                        <li>Difficulty increases gradually over 21 months</li>
                        <li>Learn different cipher and puzzle techniques</li>
                        <li>Earn points and track your progress</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="color: #2c3e50; font-size: 18px; margin: 0 0 20px 0;">Your first Sunday puzzle arrives soon!</p>
                    <a href="{settings.FRONTEND_URL}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Visit Your Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _format_solution_confirmation_email(self, week_number: int, day_of_week: str, solution: str) -> str:
        """Format solution confirmation email"""
        next_day = {'Sunday': 'Wednesday', 'Wednesday': 'Friday', 'Friday': 'next Sunday'}.get(day_of_week, 'next puzzle')
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #28a745; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">✅ Puzzle Solved!</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Week {week_number} {day_of_week}</p>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 0 0 8px 8px;">
                <div style="text-align: center; margin: 20px 0;">
                    <p style="font-size: 18px; color: #2c3e50;">🎉 Correct! Your solution:</p>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <code style="font-size: 20px; color: #28a745; font-weight: bold;">{solution}</code>
                    </div>
                    <p style="color: #6c757d;">Next challenge: {next_day}</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _format_weekly_completion_email(self, week_number: int) -> str:
        """Format weekly completion celebration email"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">🎉 Week {week_number} Complete!</h1>
                <p style="margin: 15px 0 0 0; font-size: 18px; opacity: 0.9;">All 3 puzzles solved!</p>
            </div>
            
            <div style="background: white; padding: 40px 30px; border-radius: 0 0 8px 8px; text-align: center;">
                <div style="margin: 30px 0;">
                    <div style="background: #28a745; color: white; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 40px;">🏆</div>
                    <h2 style="color: #2c3e50; margin: 0 0 15px 0;">Fantastic Work!</h2>
                    <p style="color: #6c757d; margin: 0; font-size: 16px;">You've mastered all three challenges this week. Ready for the next adventure?</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #2c3e50;"><strong>Week {week_number + 1}</strong> begins this Sunday with a new set of challenges!</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _format_weekly_summary_email(self, week_number: int, solved_days: list, missed_days: list) -> str:
        """Format weekly summary email"""
        total_solved = len(solved_days)
        progress_percent = (total_solved / 3) * 100
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #6c757d; color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">📊 Week {week_number} Summary</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Your cryptic journey progress</p>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 0 0 8px 8px;">
                <div style="text-align: center; margin: 20px 0;">
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #2c3e50; margin: 0 0 15px 0;">Progress: {total_solved}/3 puzzles solved</h3>
                        <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #28a745; height: 100%; width: {progress_percent}%; border-radius: 10px;"></div>
                        </div>
                    </div>
                    
                    {"<p style='color: #28a745; font-weight: bold;'>🎉 Perfect week! All puzzles solved!</p>" if total_solved == 3 else f"<p style='color: #dc3545;'>Missed: {', '.join(missed_days)}</p>" if missed_days else ""}
                </div>
            </div>
        </body>
        </html>
        """
