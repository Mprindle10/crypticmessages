#!/bin/bash
# Cryptic Messages Complete Setup Script
# This script sets up the database, imports content, and starts services

set -e  # Exit on any error

echo "🔐 Cryptic Messages Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is running
print_status "Checking PostgreSQL connection..."
if ! psql -d "postgresql://m:Prindle#$%10@localhost/theriddleroom" -c "SELECT 1;" > /dev/null 2>&1; then
    print_error "Cannot connect to PostgreSQL database"
    print_error "Please ensure PostgreSQL is running and the database 'theriddleroom' exists"
    exit 1
fi
print_success "PostgreSQL connection verified"

# Import database schema and content
print_status "Setting up database schema..."
psql -d "postgresql://m:Prindle#$%10@localhost/theriddleroom" -f setup_scheduler_database.sql
print_success "Scheduler database tables created"

print_status "Importing cryptic messages content..."
psql -d "postgresql://m:Prindle#$%10@localhost/theriddleroom" -f import_all_messages.sql
print_success "All 273 messages imported successfully"

# Verify content import
MESSAGE_COUNT=$(psql -d "postgresql://m:Prindle#$%10@localhost/theriddleroom" -t -c "SELECT COUNT(*) FROM cryptic_messages;" | tr -d ' ')
print_status "Verifying import: Found $MESSAGE_COUNT messages"

if [ "$MESSAGE_COUNT" -ne "273" ]; then
    print_warning "Expected 273 messages but found $MESSAGE_COUNT"
    print_warning "Some messages may not have imported correctly"
else
    print_success "All 273 messages verified in database"
fi

# Check Python dependencies
print_status "Checking Python dependencies..."
REQUIRED_PACKAGES="asyncio schedule sqlalchemy twilio sendgrid python-decouple"

for package in $REQUIRED_PACKAGES; do
    if ! python3 -c "import ${package}" 2>/dev/null; then
        print_warning "Missing Python package: $package"
        print_status "Installing $package..."
        pip3 install $package
    fi
done
print_success "Python dependencies verified"

# Set up configuration
print_status "Setting up configuration..."
if [ ! -f ".env.scheduler" ]; then
    print_warning "No .env.scheduler file found"
    print_status "Please copy .env.scheduler.example and update with your API keys"
else
    print_success "Configuration file found"
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x scheduler_manager.py
chmod +x setup_cryptic_messages.sh
print_success "Scripts are now executable"

# Create systemd service file (optional)
print_status "Creating systemd service file..."
cat > cryptic-scheduler.service << EOF
[Unit]
Description=Cryptic Messages Scheduler Service
After=network.target postgresql.service

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which python3) $(pwd)/scheduler_service.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$(pwd)

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service file created: cryptic-scheduler.service"
print_status "To install as system service, run:"
print_status "  sudo cp cryptic-scheduler.service /etc/systemd/system/"
print_status "  sudo systemctl enable cryptic-scheduler"
print_status "  sudo systemctl start cryptic-scheduler"

# Test configuration
print_status "Testing scheduler configuration..."
if python3 -c "
import sys
sys.path.append('.')
from scheduler_service import CrypticMessageScheduler
scheduler = CrypticMessageScheduler()
print('✅ Scheduler configuration test passed')
" 2>/dev/null; then
    print_success "Scheduler configuration test passed"
else
    print_warning "Scheduler configuration test failed - check your API keys"
fi

# Display next steps
echo
echo "🎉 Setup Complete!"
echo "=================="
echo
echo "Next steps:"
echo "1. Update .env.scheduler with your API keys:"
echo "   - Twilio Account SID and Auth Token"
echo "   - SendGrid API Key"
echo "   - Configure phone numbers and email addresses"
echo
echo "2. Start the scheduler service:"
echo "   python3 scheduler_manager.py start"
echo
echo "3. Check service status:"
echo "   python3 scheduler_manager.py status"
echo
echo "4. View logs:"
echo "   python3 scheduler_manager.py logs"
echo
echo "5. Test message delivery:"
echo "   python3 -c \"
from scheduler_service import CrypticMessageScheduler
import asyncio
scheduler = CrypticMessageScheduler()
asyncio.run(scheduler.send_test_message(1, 1, 'Sunday'))
\""
echo
echo "📅 Delivery Schedule:"
echo "   - Sunday: 8:00 AM"
echo "   - Wednesday: 6:00 PM"
echo "   - Friday: 3:00 PM"
echo
echo "🌐 Marketing Materials:"
echo "   - See marketing_materials.md for complete campaign content"
echo "   - Customize pricing and messaging as needed"
echo
echo "📊 Database Status:"
echo "   - Total Messages: $MESSAGE_COUNT"
echo "   - Weeks Covered: 91 weeks (21 months)"
echo "   - Difficulty Levels: 1-20"
echo
print_success "Cryptic Messages subscription service is ready to launch!"
