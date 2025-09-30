#!/usr/bin/env python3
"""
Beta Email Manager
Send welcome emails and weekly challenges to beta trial users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_service import email_service
from database import engine
from sqlalchemy import text
import argparse

def send_welcome_emails():
    """Send welcome emails to all beta users who haven't received one"""
    print("🚀 Sending welcome emails to beta trial users...")
    count = email_service.send_welcome_to_all_beta_users()
    print(f"✅ Sent welcome emails to {count} users")

def send_first_challenges():
    """Send first challenge to all beta users"""
    print("🧠 Sending first challenges to beta trial users...")
    
    with engine.connect() as conn:
        # Get all beta users
        result = conn.execute(text("""
            SELECT email FROM users 
            WHERE subscription_type = 'beta_trial'
            ORDER BY created_at DESC
        """))
        
        users = result.fetchall()
        sent_count = 0
        
        for user in users:
            email = user[0]
            success = email_service.send_first_challenge(email)
            if success:
                sent_count += 1
                print(f"✅ Sent challenge to {email}")
            else:
                print(f"❌ Failed to send to {email}")
        
        print(f"📧 First challenges sent to {sent_count} users")

def list_beta_users():
    """List all beta trial users"""
    print("📋 Beta Trial Users:")
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, email, experience, created_at 
            FROM users 
            WHERE subscription_type = 'beta_trial'
            ORDER BY created_at DESC
        """))
        
        users = result.fetchall()
        
        if not users:
            print("No beta users found.")
            return
        
        for user in users:
            user_id, email, experience, created_at = user
            print(f"ID: {user_id} | {email} | {experience} | {created_at}")
        
        print(f"\nTotal beta users: {len(users)}")

def setup_email_config():
    """Help setup email configuration for cryptic message service"""
    print("� SendGrid Single Sender Setup for The Riddle Room")
    print("=" * 55)
    print("⚠️  IMPORTANT: Skip DNS records - use Single Sender instead!")
    print()
    print("🚀 Quick Setup (5 minutes):")
    print("1. Go to: https://app.sendgrid.com/settings/sender_auth")
    print("2. Click 'Verify a Single Sender'")
    print("3. Enter: crypticmessageswithallmighty1@gmail.com")
    print("4. Check Gmail for verification email")
    print("5. Get API key: https://app.sendgrid.com/settings/api_keys")
    print("6. Update .env: SENDGRID_API_KEY=SG.your-key")
    print()
    print("📧 Your Beta Users Waiting:")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT email FROM users WHERE subscription_type = 'beta_trial'"))
            users = result.fetchall()
            for i, user in enumerate(users, 1):
                print(f"   {i}. {user[0]}")
    except Exception:
        print("   (Check database for beta users)")
    print()
    print("🔐 Sunday's First Challenge Ready:")
    print("   WKLV LV MXVW WKH EHJLQQLQJ")
    print("   (Caesar Cipher - shift 3)")
    print()
    print("✅ Test when ready: python3 beta_email_manager.py welcome")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage beta trial emails")
    parser.add_argument("action", choices=[
        "welcome", "challenge", "list", "config"
    ], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "welcome":
        send_welcome_emails()
    elif args.action == "challenge":
        send_first_challenges()
    elif args.action == "list":
        list_beta_users()
    elif args.action == "config":
        setup_email_config()
