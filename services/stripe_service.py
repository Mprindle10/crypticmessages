import stripe
from app.core.config import settings
from app.database import get_db
from app.models.user import User
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    async def create_subscription(customer_email: str, price_id: str) -> dict:
        """Create a new subscription for tri-weekly cryptic messages"""
        try:
            # Create or retrieve customer
            customers = stripe.Customer.list(email=customer_email, limit=1)
            
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(
                    email=customer_email,
                    description=f"Cryptic Messages subscriber: {customer_email}",
                    metadata={
                        'service': 'cryptic_messages',
                        'delivery_frequency': 'tri_weekly',
                        'subscription_type': '21_month_journey'
                    }
                )
            
            # Create subscription for tri-weekly delivery
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    'price': price_id,
                }],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
                metadata={
                    'delivery_schedule': 'sunday_wednesday_friday',
                    'total_messages': '273',  # 91 weeks × 3 messages
                    'journey_length': '21_months'
                }
            )
            
            return {
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret,
                'customer_id': customer.id,
                'delivery_schedule': 'Sunday, Wednesday, Friday'
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating subscription: {str(e)}")
            raise Exception(f"Payment processing error: {str(e)}")
    
    @staticmethod
    async def handle_webhook(payload: bytes, signature: str) -> dict:
        """Handle Stripe webhooks for subscription events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            
            event_type = event['type']
            logger.info(f"Processing Stripe webhook: {event_type}")
            
            if event_type == 'invoice.payment_succeeded':
                return await StripeService._handle_payment_success(event['data']['object'])
            elif event_type == 'invoice.payment_failed':
                return await StripeService._handle_payment_failed(event['data']['object'])
            elif event_type == 'customer.subscription.deleted':
                return await StripeService._handle_subscription_cancelled(event['data']['object'])
            elif event_type == 'customer.subscription.updated':
                return await StripeService._handle_subscription_updated(event['data']['object'])
            
            return {'status': 'ignored', 'event_type': event_type}
            
        except ValueError as e:
            logger.error(f"Invalid payload in webhook: {str(e)}")
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature in webhook: {str(e)}")
            raise Exception("Invalid signature")
    
    @staticmethod
    async def _handle_payment_success(invoice) -> dict:
        """Handle successful payment and activate tri-weekly delivery"""
        customer_id = invoice['customer']
        subscription_id = invoice['subscription']
        
        # Update user subscription status in database
        db = next(get_db())
        customer = stripe.Customer.retrieve(customer_id)
        user = db.query(User).filter(User.email == customer.email).first()
        
        if user:
            user.subscription_id = subscription_id
            user.is_active = True
            user.subscription_start_date = datetime.utcnow()
            
            # Initialize user progress for tri-weekly system
            from app.models.user_progress import UserProgress
            progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
            if not progress:
                progress = UserProgress(
                    user_id=user.id,
                    current_week=1,
                    total_solved=0,
                    total_points=0,
                    longest_streak=0,
                    current_streak=0
                )
                db.add(progress)
            
            db.commit()
            logger.info(f"Activated tri-weekly subscription for user: {user.email}")
            
            # Send welcome messages via both SMS and email
            from services.twilio_service import TwilioService
            from services.sendgrid_service import SendGridService
            
            twilio = TwilioService()
            sendgrid = SendGridService()
            
            if user.phone:
                await twilio.send_subscription_welcome(user.phone)
            await sendgrid.send_welcome_email(user.email)
        
        return {
            'status': 'payment_success', 
            'user_email': customer.email,
            'delivery_schedule': 'tri_weekly'
        }
    
    @staticmethod
    async def _handle_payment_failed(invoice) -> dict:
        """Handle failed payment"""
        customer_id = invoice['customer']
        customer = stripe.Customer.retrieve(customer_id)
        
        # Update user status with grace period for tri-weekly service
        db = next(get_db())
        user = db.query(User).filter(User.email == customer.email).first()
        
        if user:
            # Set grace period end date (e.g., 7 days)
            user.grace_period_end = datetime.utcnow() + timedelta(days=7)
            db.commit()
            logger.warning(f"Payment failed for tri-weekly user: {user.email}, grace period set")
        
        return {'status': 'payment_failed', 'user_email': customer.email}
    
    @staticmethod
    async def _handle_subscription_cancelled(subscription) -> dict:
        """Handle subscription cancellation"""
        customer_id = subscription['customer']
        customer = stripe.Customer.retrieve(customer_id)
        
        db = next(get_db())
        user = db.query(User).filter(User.email == customer.email).first()
        
        if user:
            user.is_active = False
            user.subscription_id = None
            user.subscription_end_date = datetime.utcnow()
            db.commit()
            logger.info(f"Deactivated tri-weekly subscription for user: {user.email}")
        
        return {'status': 'subscription_cancelled', 'user_email': customer.email}
    
    @staticmethod
    async def _handle_subscription_updated(subscription) -> dict:
        """Handle subscription updates"""
        customer_id = subscription['customer']
        customer = stripe.Customer.retrieve(customer_id)
        
        db = next(get_db())
        user = db.query(User).filter(User.email == customer.email).first()
        
        if user:
            # Update subscription status based on current status
            user.is_active = subscription['status'] == 'active'
            db.commit()
            logger.info(f"Updated subscription status for user: {user.email}, status: {subscription['status']}")
        
        return {
            'status': 'subscription_updated', 
            'user_email': customer.email,
            'subscription_status': subscription['status']
        }
    
    @staticmethod
    async def get_subscription_stats(subscription_id: str) -> Dict:
        """Get statistics for a tri-weekly subscription"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Calculate journey progress
            start_date = datetime.fromtimestamp(subscription.created)
            current_date = datetime.utcnow()
            weeks_elapsed = (current_date - start_date).days // 7
            
            total_weeks = 91  # 21 months
            total_messages = 273  # 91 weeks × 3 messages
            messages_sent = min(weeks_elapsed * 3, total_messages)
            
            progress_percentage = (weeks_elapsed / total_weeks) * 100
            
            return {
                'subscription_id': subscription_id,
                'status': subscription.status,
                'weeks_elapsed': weeks_elapsed,
                'total_weeks': total_weeks,
                'messages_sent': messages_sent,
                'total_messages': total_messages,
                'progress_percentage': min(progress_percentage, 100),
                'delivery_schedule': 'Sunday, Wednesday, Friday',
                'journey_completion_date': start_date + timedelta(weeks=91)
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving subscription stats: {str(e)}")
            raise Exception(f"Unable to retrieve subscription information: {str(e)}")
