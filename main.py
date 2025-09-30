"""
Cryptic Messages Subscription Service - FastAPI Backend
Full-stack cryptic message subscription service with FastAPI, PostgreSQL, Twilio & SendGrid
"""

import os
import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, ValidationError
import stripe
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

# Import your database setup
from database import get_db, engine
from models import User, CrypticMessage, UserProgress, UserSubmission

# Import services (we'll make these optional for now)
try:
    from welcome_email_service import WelcomeEmailService
    welcome_service = None  # Will initialize later when needed
except ImportError:
    welcome_service = None

try:
    from scheduler_service import SchedulerService
    scheduler_service = None  # Will initialize later when needed
except ImportError:
    scheduler_service = None

try:
    from email_service import email_service
    print("Email service loaded successfully")
except ImportError:
    email_service = None
    print("Email service not available")

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Cipher Academy - Cryptic Messages API",
    description="Full-stack cryptic message subscription service with 273 progressive challenges",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include welcome email routes (optional)
try:
    from welcome_email_api import router as welcome_router
    app.include_router(welcome_router, prefix="/api/welcome", tags=["welcome-emails"])
except ImportError:
    print("Warning: welcome_email_api not available")

# Initialize services (made optional)
# welcome_service and scheduler_service are imported above

# Pydantic models
class EmailSubscription(BaseModel):
    email: EmailStr
    plan: str = "free_trial"
    source: str = "website"
    phone: str = None
    experience: str = "beginner"
    motivation: str = None
    background: str = None

class PaidSubscription(BaseModel):
    email: EmailStr
    plan_id: str
    payment_method_id: str = None

class ChallengeSubmission(BaseModel):
    week_number: int
    user_answer: str
    hint_used: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    subscription_type: str
    current_week: int
    total_points: int
    current_streak: int

# Beta landing page
@app.get("/beta", response_class=HTMLResponse)
async def beta_landing():
    """Serve beta landing page"""
    try:
        with open("beta_landing_page.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Beta landing page not found</h1>")

# Beta success page
@app.get("/beta/success", response_class=HTMLResponse)
async def beta_success():
    """Serve beta success page"""
    try:
        with open("beta_success.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Success page not found</h1>")

# Root endpoint
@app.get("/")
async def root():
    """Welcome to Cipher Academy API"""
    return {
        "message": "Welcome to Cipher Academy - Your Journey into Cryptography Awaits! 🔐",
        "version": "1.0.0",
        "total_challenges": 273,
        "journey_duration": "21 months",
        "api_docs": "/docs"
    }

# Health check
@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "database": "connected",
            "services": "running"
        }
    except Exception as e:
        print(f"DEBUG: Health check error: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")

# User subscription endpoints
@app.post("/api/subscribe", response_model=dict)
async def create_subscription(
    subscription: EmailSubscription, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle free trial and paid subscriptions"""
    try:
        print(f"DEBUG: Received subscription data: {subscription}")  # Debug log
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == subscription.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = User(
            email=subscription.email,
            subscription_type=subscription.plan,
            signup_source=subscription.source,
            phone=subscription.phone,
            experience=subscription.experience,
            motivation=subscription.motivation,
            background=subscription.background,
            created_at=datetime.now(),
            is_active=True,
            current_week=1,
            total_points=0,
            current_streak=0
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Initialize user progress
        user_progress = UserProgress(
            user_id=new_user.id,
            current_week=1,
            total_solved=0,
            total_points=0,
            current_streak=0,
            last_activity=datetime.now()
        )
        db.add(user_progress)
        db.commit()
        
        # Send welcome email for beta trial users
        if subscription.plan == "beta_trial" and email_service:
            background_tasks.add_task(
                email_service.send_welcome_email,
                new_user.email,
                subscription.experience
            )
            print(f"Scheduled welcome email for beta user: {new_user.email}")
        
        # Schedule welcome email series for other users
        if welcome_service:
            background_tasks.add_task(
                welcome_service.schedule_welcome_series, 
                new_user.email, 
                new_user.id
            )
        
        # For free trial, schedule first week's messages
        if subscription.plan == "free_trial" and scheduler_service:
            background_tasks.add_task(
                scheduler_service.schedule_week_messages,
                new_user.id,
                1  # Week 1
            )
        
        return {
            "success": True,
            "message": "Welcome to Cipher Academy! Check your email for your first challenge.",
            "user_id": new_user.id,
            "next_step": "check_email",
            "welcome_series": "7 emails over 14 days"
        }
        
    except ValidationError as e:
        print(f"DEBUG: Validation error: {e}")
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Invalid data: {e}")
    except Exception as e:
        print(f"DEBUG: Subscription error: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/create-checkout-session")
async def create_checkout_session(subscription: PaidSubscription):
    """Create Stripe checkout session for paid subscriptions"""
    try:
        # Define pricing plans
        price_map = {
            "monthly": {
                "price": 1999,  # $19.99/month
                "interval": "month",
                "description": "Monthly access to all 273 cryptic challenges"
            },
            "era": {
                "price": 8900,  # $89 one-time
                "interval": None,
                "description": "Complete Era Bundle - All challenges + bonus content"
            },
            "full": {
                "price": 1400,  # $14/month for 21 months
                "interval": "month",
                "interval_count": 21,
                "description": "Full 21-Month Cipher Academy Journey"
            }
        }
        
        plan_config = price_map.get(subscription.plan_id)
        if not plan_config:
            raise HTTPException(status_code=400, detail="Invalid subscription plan")
        
        # Create Stripe checkout session
        if plan_config["interval"]:
            # Subscription plans
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Cipher Academy - {subscription.plan_id.title()} Plan',
                        'description': plan_config["description"],
                    },
                    'unit_amount': plan_config["price"],
                    'recurring': {
                        'interval': plan_config["interval"],
                    },
                },
                'quantity': 1,
            }
            
            # Add interval_count for limited subscriptions
            if "interval_count" in plan_config:
                line_item['price_data']['recurring']['interval_count'] = plan_config["interval_count"]
                
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[line_item],
                mode='subscription',
                success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:3000/pricing',
                customer_email=subscription.email,
                metadata={
                    'plan_id': subscription.plan_id,
                    'email': subscription.email
                }
            )
        else:
            # One-time payment (Era bundle)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Cipher Academy - {subscription.plan_id.title()} Bundle',
                            'description': plan_config["description"],
                        },
                        'unit_amount': plan_config["price"],
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:3000/pricing',
                customer_email=subscription.email,
                metadata={
                    'plan_id': subscription.plan_id,
                    'email': subscription.email
                }
            )
        
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id,
            "plan": subscription.plan_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Challenge submission endpoint
@app.post("/api/submit-challenge")
async def submit_challenge(
    submission: ChallengeSubmission,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Submit answer for a cryptic challenge"""
    try:
        # Get user and current challenge
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        challenge = db.query(CrypticMessage).filter(
            CrypticMessage.week_number == submission.week_number
        ).first()
        
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        
        # Check if answer is correct
        is_correct = submission.user_answer.upper().strip() == challenge.answer.upper().strip()
        
        # Calculate points
        base_points = challenge.points_value
        points_earned = 0
        
        if is_correct:
            points_earned = base_points
            if submission.hint_used:
                points_earned = int(base_points * 0.7)  # 30% penalty for using hint
        
        # Create submission record
        user_submission = UserSubmission(
            user_id=user_id,
            week_number=submission.week_number,
            user_answer=submission.user_answer,
            is_correct=is_correct,
            points_earned=points_earned,
            hint_used=submission.hint_used,
            submitted_at=datetime.now()
        )
        
        db.add(user_submission)
        
        # Update user progress if correct
        if is_correct:
            user_progress = db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).first()
            
            if user_progress:
                user_progress.total_solved += 1
                user_progress.total_points += points_earned
                user_progress.current_streak += 1
                user_progress.last_activity = datetime.now()
                
                # Advance to next week if this was current week
                if submission.week_number == user_progress.current_week:
                    user_progress.current_week += 1
        
        db.commit()
        
        return {
            "success": True,
            "correct": is_correct,
            "points_earned": points_earned,
            "message": "Excellent work! 🎉" if is_correct else "Not quite right. Try again! 🤔",
            "next_challenge": submission.week_number + 1 if is_correct else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get user progress
@app.get("/api/user/{user_id}/progress", response_model=UserResponse)
async def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """Get user's current progress"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    
    return UserResponse(
        id=user.id,
        email=user.email,
        subscription_type=user.subscription_type,
        current_week=progress.current_week if progress else 1,
        total_points=progress.total_points if progress else 0,
        current_streak=progress.current_streak if progress else 0
    )

# Get current week's challenges
@app.get("/api/challenges/week/{week_number}")
async def get_week_challenges(week_number: int, db: Session = Depends(get_db)):
    """Get challenges for a specific week"""
    challenges = db.query(CrypticMessage).filter(
        CrypticMessage.week_number == week_number
    ).all()
    
    if not challenges:
        raise HTTPException(status_code=404, detail="No challenges found for this week")
    
    # Don't return answers in the response
    return [{
        "id": challenge.id,
        "week_number": challenge.week_number,
        "day_of_week": challenge.day_of_week,
        "title": challenge.title,
        "content": challenge.content,
        "difficulty_level": challenge.difficulty_level,
        "points_value": challenge.points_value,
        "hint": challenge.hint
    } for challenge in challenges]

# Admin endpoint to trigger scheduler
@app.post("/api/admin/process-scheduled-messages")
async def process_scheduled_messages(background_tasks: BackgroundTasks):
    """Manually trigger scheduled message processing (admin only)"""
    if scheduler_service:
        background_tasks.add_task(scheduler_service.process_scheduled_messages)
        return {"message": "Scheduled message processing initiated"}
    else:
        return {"message": "Scheduler service not available"}

# Webhook endpoint for Stripe
@app.post("/api/webhooks/stripe")
async def stripe_webhook(request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events"""
    # TODO: Implement Stripe webhook handling for payment confirmations
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
