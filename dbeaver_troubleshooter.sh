#!/bin/bash

echo "🔧 DBeaver PostgreSQL Connection Troubleshooter"
echo "==============================================="

# Test 1: Verify PostgreSQL is accessible
echo "1. Testing direct PostgreSQL connection..."
if PGPASSWORD='Prindle#$%10' psql -h localhost -U m -d theriddleroom -c "SELECT 'Database accessible' as status;" 2>/dev/null; then
    echo "✅ PostgreSQL database is accessible"
else
    echo "❌ PostgreSQL connection failed"
    exit 1
fi

# Test 2: Check Java version (required for JDBC)
echo -e "\n2. Checking Java installation..."
if java -version 2>&1 | head -1; then
    echo "✅ Java is installed"
else
    echo "❌ Java not found - installing..."
    sudo apt update && sudo apt install -y default-jre
fi

# Test 3: Download multiple JDBC driver versions
echo -e "\n3. Downloading PostgreSQL JDBC drivers..."

# Current version
if [ ! -f "postgresql-42.7.1.jar" ]; then
    wget -q https://jdbc.postgresql.org/download/postgresql-42.7.1.jar
    echo "✅ Downloaded postgresql-42.7.1.jar"
fi

# Older stable version (sometimes works better)
if [ ! -f "postgresql-42.6.0.jar" ]; then
    wget -q https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
    echo "✅ Downloaded postgresql-42.6.0.jar (alternative)"
fi

# Test 4: Create alternative connection URLs
echo -e "\n4. Alternative JDBC URLs to try in DBeaver:"
echo "   Standard:     jdbc:postgresql://localhost:5432/theriddleroom"
echo "   With SSL off: jdbc:postgresql://localhost:5432/theriddleroom?ssl=false"
echo "   With timeout: jdbc:postgresql://localhost:5432/theriddleroom?ssl=false&loginTimeout=30"
echo "   IPv4 only:    jdbc:postgresql://127.0.0.1:5432/theriddleroom?ssl=false"

# Test 5: Check DBeaver installation
echo -e "\n5. DBeaver troubleshooting:"
if command -v dbeaver-ce &> /dev/null; then
    echo "✅ DBeaver Community Edition found"
    echo "   Version: $(snap info dbeaver-ce | grep 'installed:' | cut -d' ' -f2)"
else
    echo "❌ DBeaver not found via snap"
    echo "   Install with: sudo snap install dbeaver-ce"
fi

# Test 6: Create DBeaver connection profile
echo -e "\n6. Creating DBeaver connection profile..."
mkdir -p ~/.local/share/DBeaverData/workspace6/.metadata/.plugins/org.jkiss.dbeaver.core/

cat > dbeaver_connection_template.txt << EOF
DBeaver Connection Settings for Cipher Academy:

Connection Name: Cipher Academy Database
Connection Type: PostgreSQL
Driver: PostgreSQL

Main Tab:
├── Server Host: localhost
├── Port: 5432
├── Database: theriddleroom
├── Username: m
├── Password: Prindle#\$%10
└── Save password: ✓

Driver Properties:
├── ssl: false
├── loginTimeout: 30
└── socketTimeout: 60

JDBC URL Examples:
1. jdbc:postgresql://localhost:5432/theriddleroom
2. jdbc:postgresql://localhost:5432/theriddleroom?ssl=false
3. jdbc:postgresql://127.0.0.1:5432/theriddleroom?ssl=false&loginTimeout=30

Manual Driver Path:
$(pwd)/postgresql-42.7.1.jar
$(pwd)/postgresql-42.6.0.jar
EOF

echo "✅ Connection template created: dbeaver_connection_template.txt"

# Test 7: Verify database content
echo -e "\n7. Verifying Cipher Academy database content..."
echo "📊 Database overview:"
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

echo -e "\n8. Testing specific table access:"
echo "📧 Checking for welcome email tables..."
PGPASSWORD='Prindle#$%10' psql -h localhost -U m -d theriddleroom -c "
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename LIKE '%email%';" 2>/dev/null || echo "❌ Welcome email tables not found - run setup_welcome_emails.sh"

echo ""
echo "🎯 Next Steps for DBeaver:"
echo "=========================="
echo "1. Use the downloaded JDBC drivers in DBeaver's Driver Manager"
echo "2. Try each JDBC URL format listed above"
echo "3. If still failing, try DBeaver Ultimate Edition trial"
echo "4. Alternative: Use pgAdmin4 instead of DBeaver"
echo ""
echo "📁 Files created:"
echo "  - postgresql-42.7.1.jar (main driver)"
echo "  - postgresql-42.6.0.jar (alternative)"
echo "  - dbeaver_connection_template.txt (configuration guide)"
echo ""
echo "🔐 Your Cipher Academy database is ready - just need to connect DBeaver!"
EOF

chmod +x dbeaver_troubleshooter.sh
./dbeaver_troubleshooter.sh
