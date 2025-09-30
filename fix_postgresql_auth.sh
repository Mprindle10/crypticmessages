#!/bin/bash

echo "🔐 Fixing PostgreSQL Authentication for Cipher Academy Database"
echo "============================================================"

# Step 1: Check PostgreSQL status
echo "1. Checking PostgreSQL service..."
sudo systemctl status postgresql --no-pager -l

# Step 2: Connect as postgres superuser to fix authentication
echo -e "\n2. Fixing user 'm' authentication..."
sudo -u postgres psql << EOF
-- Reset password for user 'm'
ALTER USER m WITH PASSWORD 'Prindle#\$%10';

-- Ensure user has proper privileges
GRANT ALL PRIVILEGES ON DATABASE theriddleroom TO m;

-- Make user a superuser for full access
ALTER USER m CREATEDB CREATEROLE;

-- Show current users
\du

-- Exit
\q
EOF

# Step 3: Update pg_hba.conf for authentication
echo -e "\n3. Updating PostgreSQL authentication configuration..."

# Backup original pg_hba.conf
sudo cp /etc/postgresql/16/main/pg_hba.conf /etc/postgresql/16/main/pg_hba.conf.backup

# Update authentication method
sudo sed -i 's/local   all             all                                     peer/local   all             all                                     md5/' /etc/postgresql/16/main/pg_hba.conf

# Add specific rules for your database
echo "# Cipher Academy Database Access" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
echo "host    theriddleroom   m               127.0.0.1/32            md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
echo "host    theriddleroom   m               ::1/128                 md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf

# Step 4: Restart PostgreSQL
echo -e "\n4. Restarting PostgreSQL service..."
sudo systemctl restart postgresql

# Wait for service to start
sleep 3

# Step 5: Test connection
echo -e "\n5. Testing connection to Cipher Academy database..."
export PGPASSWORD='Prindle#$%10'

if psql -h localhost -U m -d theriddleroom -c "SELECT 'Connection successful! 🎉' AS status;" 2>/dev/null; then
    echo "✅ Authentication fixed successfully!"
else
    echo "❌ Authentication still failing. Trying alternative method..."
    
    # Alternative: Create .pgpass file
    echo "localhost:5432:theriddleroom:m:Prindle#\$%10" > ~/.pgpass
    chmod 600 ~/.pgpass
    
    if psql -h localhost -U m -d theriddleroom -c "SELECT 'Connection with .pgpass successful! 🎉' AS status;" 2>/dev/null; then
        echo "✅ Authentication fixed with .pgpass file!"
    else
        echo "❌ Still having issues. Manual intervention required."
    fi
fi

# Step 6: Verify database structure
echo -e "\n6. Verifying Cipher Academy database structure..."
export PGPASSWORD='Prindle#$%10'

echo "📊 Database tables:"
psql -h localhost -U m -d theriddleroom -c "
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;" 2>/dev/null || echo "❌ Cannot access database tables"

echo -e "\n📧 Welcome email integration status:"
psql -h localhost -U m -d theriddleroom -c "
SELECT 
    'Email Templates' as component,
    count(*) as count
FROM email_templates
UNION ALL
SELECT 
    'Welcome Email Series',
    count(*)
FROM welcome_email_series;" 2>/dev/null || echo "❌ Welcome email tables not found - run setup_welcome_emails.sh"

echo -e "\n🔐 Cryptic messages status:"
psql -h localhost -U m -d theriddleroom -c "
SELECT 
    'Total Messages' as component,
    count(*) as count
FROM cryptic_messages;" 2>/dev/null || echo "❌ Cryptic messages table not found"

echo ""
echo "🎯 DBeaver Connection Settings:"
echo "================================="
echo "Host: localhost"
echo "Port: 5432"
echo "Database: theriddleroom"
echo "Username: m"
echo "Password: Prindle#\$%10"
echo "Driver: PostgreSQL"
echo "URL: jdbc:postgresql://localhost:5432/theriddleroom"
echo ""
echo "🚀 Your Cipher Academy database is ready for DBeaver!"
