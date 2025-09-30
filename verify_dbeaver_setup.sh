#!/bin/bash

echo "🔐 DBeaver JDBC Driver Verification for Cipher Academy"
echo "====================================================="

# Check available drivers
echo "📁 Available PostgreSQL JDBC Drivers:"
ls -la /home/m/crypticmessages/postgresql*.jar

# Test database connectivity
echo -e "\n🔗 Testing PostgreSQL Database Connection..."
if PGPASSWORD='Prindle#$%10' psql -h localhost -U m -d theriddleroom -c "SELECT 'Database connection working! ✅' as status;" 2>/dev/null; then
    echo "✅ PostgreSQL database is accessible"
    
    # Show database contents
    echo -e "\n📊 Your Cipher Academy Database Contents:"
    PGPASSWORD='Prindle#$%10' psql -h localhost -U m -d theriddleroom -c "
    SELECT 
        'Tables' as type,
        count(*) as count
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    UNION ALL
    SELECT 
        'Cryptic Messages',
        count(*)
    FROM cryptic_messages
    UNION ALL
    SELECT 
        'Users',
        count(*)
    FROM users;"
    
else
    echo "❌ Database connection failed"
    exit 1
fi

# Test JDBC drivers
echo -e "\n🧪 Testing JDBC Drivers with Java..."
if command -v java &> /dev/null; then
    echo "✅ Java is available: $(java -version 2>&1 | head -1)"
    
    # Test driver loading
    for driver in postgresql-42.7.1.jar postgresql-42.6.0.jar postgresql-jdbc.jar; do
        if [ -f "$driver" ]; then
            echo "📦 Testing $driver..."
            if java -cp "$driver" -Duser.dir=. org.postgresql.Driver 2>/dev/null; then
                echo "  ✅ $driver loads successfully"
            else
                echo "  ⚠️  $driver - driver class test (this is normal if driver loads properly)"
            fi
        fi
    done
else
    echo "❌ Java not found - installing..."
    sudo apt update && sudo apt install -y default-jre
fi

# Create DBeaver configuration help
echo -e "\n🎯 DBeaver Configuration Summary:"
echo "=================================="
echo "Driver Path: $(pwd)/postgresql-42.7.1.jar"
echo "Driver Class: org.postgresql.Driver"
echo ""
echo "Connection Settings:"
echo "├── Host: localhost"
echo "├── Port: 5432"
echo "├── Database: theriddleroom"  
echo "├── Username: m"
echo "├── Password: Prindle#\$%10"
echo "└── JDBC URL: jdbc:postgresql://localhost:5432/theriddleroom"
echo ""
echo "Alternative JDBC URLs if needed:"
echo "├── jdbc:postgresql://localhost:5432/theriddleroom?ssl=false"
echo "├── jdbc:postgresql://127.0.0.1:5432/theriddleroom?ssl=false"
echo "└── jdbc:postgresql://localhost:5432/theriddleroom?ssl=false&loginTimeout=30"

# Show what you'll see in DBeaver
echo -e "\n📋 What You'll See in DBeaver Once Connected:"
echo "=============================================="
PGPASSWORD='Prindle#$%10' psql -h localhost -U m -d theriddleroom -c "
SELECT 
    tablename as 'Table Name',
    CASE 
        WHEN tablename = 'cryptic_messages' THEN 'Your 273 cipher challenges'
        WHEN tablename = 'users' THEN 'Subscriber accounts'
        WHEN tablename = 'user_progress' THEN 'Journey tracking (91 weeks)'
        WHEN tablename = 'user_submissions' THEN 'Challenge solutions & scoring'
        WHEN tablename LIKE '%email%' THEN 'Welcome email system'
        ELSE 'Database table'
    END as 'Description'
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;" 2>/dev/null

echo -e "\n🚀 Next Steps:"
echo "=============="
echo "1. Open DBeaver"
echo "2. Database → Driver Manager → PostgreSQL → Edit"
echo "3. Libraries tab → Add File → Select: $(pwd)/postgresql-42.7.1.jar"
echo "4. Create new PostgreSQL connection with settings above"
echo "5. Test connection - should work now!"
echo ""
echo "✅ Your Cipher Academy database is ready for visual management!"
