# 🏛️ The Riddle Room - Cryptic Message Subscription Service

A full-stack subscription service that delivers progressive cryptographic challenges to users via email and SMS. Master 5,000 years of secret codes through expertly crafted puzzles.

## 🎯 Project Overview

**The Riddle Room** by Cipher Academy is an educational subscription service that teaches cryptography through progressive challenges. Users receive weekly puzzles that build upon previous solutions, creating an interconnected learning experience from ancient Caesar ciphers to modern encryption.

## 🚀 Features

### Core Functionality
- ✅ **Progressive Challenge System** - 273 challenges over 21 months
- ✅ **Multi-tier Subscriptions** - Free trial, Full Academy, Premium
- ✅ **Email & SMS Delivery** - Automated via SendGrid and Twilio
- ✅ **Beta Testing Program** - Exclusive early access
- ✅ **YouTube Marketing** - Automated video generation for promotion

### Technical Features
- ✅ **FastAPI Backend** - Modern Python web framework
- ✅ **React Frontend** - Professional landing pages
- ✅ **PostgreSQL Database** - User management and progress tracking
- ✅ **SendGrid Integration** - Professional email delivery
- ✅ **Stripe Integration** - Payment processing (planned)
- ✅ **Automated Video Generation** - YouTube Shorts for marketing

## 🏗️ Architecture

```
crypticmessages/
├── main.py                 # FastAPI backend server
├── models.py              # SQLAlchemy database models
├── database.py            # Database configuration
├── email_service.py       # SendGrid email automation
├── beta_email_manager.py  # Beta user management
├── .env                   # Environment configuration
├── frontend/              # React frontend
│   ├── src/
│   ├── public/
│   └── netlify.toml       # Netlify deployment config
├── beta_landing_page.html # Beta signup page
├── beta_success.html      # Post-signup success page
└── youtube_short_video.html # Marketing video generator
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **PostgreSQL** - Production database
- **SendGrid** - Email delivery service
- **Twilio** - SMS delivery service (planned)
- **Pydantic** - Data validation and serialization

### Frontend
- **React** - User interface library
- **HTML/CSS/JavaScript** - Landing pages and forms
- **Netlify** - Static site hosting

### DevOps & Deployment
- **Git** - Version control
- **GitHub** - Code repository
- **Netlify** - Frontend deployment
- **Ngrok** - Local development tunneling

## 📦 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/crypticmessages.git
cd crypticmessages
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart sendgrid

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 3. Database Setup
```bash
# Install PostgreSQL and create database
createdb theriddleroom

# Run database migrations
psql -U your_user -d theriddleroom -f db_schema.sql
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm start  # Development server
npm run build  # Production build
```

### 5. Start Backend Server
```bash
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/theriddleroom

# SendGrid Email
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
FROM_NAME=The Riddle Room
```

## 🚀 Deployment

### Frontend (Netlify)
1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Deploy automatically on push to main branch

## 🎮 Usage

### Beta Program Management
```bash
# List beta users
python3 beta_email_manager.py list

# Send welcome emails
python3 beta_email_manager.py welcome

# Send challenges
python3 beta_email_manager.py challenge
```

## 📊 Current Status

### Beta Program
- ✅ 3 active beta users in PostgreSQL database
- ✅ SendGrid email service configured
- ✅ Welcome email templates ready
- ✅ Sunday challenge emails scheduled

### Infrastructure
- ✅ FastAPI backend running on localhost:8000
- ✅ React frontend ready for Netlify deployment
- ✅ PostgreSQL database with user management
- ✅ YouTube video generation system

This project is a full-stack web application for sending cryptic messages to subscribers via SMS and email. Users pay a $15/month subscription fee to receive three cryptic messages each week. Each message requires the previous week's code to solve, and the difficulty increases over time.

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: React
- Database: PostgreSQL
- SMS: Twilio
- Email: SendGrid
- Payments: Stripe

## Features
- User registration and login
- Subscription management
- Weekly cryptic message generation and delivery
- Message encryption and code chaining
- Admin dashboard for message management

## Getting Started
- Backend setup: Python virtual environment, FastAPI, PostgreSQL
- Frontend setup: React app in `/frontend`
- Configure Twilio, SendGrid, and Stripe credentials

## License
MIT
