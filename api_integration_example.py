"""
Example API Integration for Frontend
Add these endpoints to your FastAPI backend (main.py)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import stripe
import os

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class EmailSubscription(BaseModel):
    email: EmailStr
    plan: str = "free_trial"
    source: str = "website"

class PaidSubscription(BaseModel):
    email: EmailStr
    plan_id: str
    payment_method_id: str

app = FastAPI()

@app.post("/api/subscribe")
async def create_email_subscription(subscription: EmailSubscription):
    """Handle free email subscription from hero form"""
    try:
        # 1. Add to database
        user_data = {
            "email": subscription.email,
            "subscription_type": subscription.plan,
            "signup_source": subscription.source,
            "created_at": datetime.now(),
            "status": "pending_confirmation"
        }
        
        # TODO: Insert into your PostgreSQL database
        # user_id = await create_user(user_data)
        
        # 2. Send to email service (SendGrid)
        await send_welcome_email(subscription.email, subscription.plan)
        
        # 3. Add to scheduled message delivery
        if subscription.plan == "free_trial":
            await schedule_week_1_messages(subscription.email)
        
        return {
            "success": True,
            "message": "Subscription created successfully",
            "next_step": "check_email"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/create-checkout-session")
async def create_checkout_session(subscription: PaidSubscription):
    """Create Stripe checkout session for paid subscriptions"""
    try:
        # Define pricing based on plan
        price_map = {
            "monthly": {"price": 1999, "interval": "month"},  # $19.99/month
            "era": {"price": 8900, "interval": None},         # $89 one-time
            "full": {"price": 1400, "interval": "month", "count": 21}  # $14/month for 21 months
        }
        
        plan_config = price_map.get(subscription.plan_id)
        if not plan_config:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        # Create Stripe checkout session
        if plan_config["interval"]:
            # Subscription
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Cipher Academy - {subscription.plan_id.title()} Plan',
                        },
                        'unit_amount': plan_config["price"],
                        'recurring': {
                            'interval': plan_config["interval"],
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://your-domain.com/cancel',
                customer_email=subscription.email,
            )
        else:
            # One-time payment
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Cipher Academy - {subscription.plan_id.title()} Plan',
                        },
                        'unit_amount': plan_config["price"],
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://your-domain.com/cancel',
                customer_email=subscription.email,
            )
        
        return {"checkout_url": checkout_session.url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def send_welcome_email(email: str, plan: str):
    """Send welcome email using SendGrid"""
    # TODO: Implement SendGrid email sending
    # Use your sendgrid_service.py
    pass

async def schedule_week_1_messages(email: str):
    """Schedule the first week of cryptic messages"""
    # TODO: Add user to scheduler_service.py delivery queue
    pass
