# DBeaver Plugin Installation Guide for Cryptic Message Service
# Follow these steps to install essential plugins for database management

## 🔌 Plugin Installation Steps

### 1. ERD Plugin - Visualize Database Relationships

**Installation:**
1. Open DBeaver
2. Go to `Help` → `Install New Software...`
3. Click `Add...` button
4. Add Repository:
   - Name: `DBeaver ERD`
   - Location: `https://dbeaver.io/update/latest/`
5. Click `OK`
6. Select `DBeaver ERD` from the list
7. Click `Next` → `Next` → `Finish`
8. Restart DBeaver when prompted

**Usage for Your Cryptic Message Service:**
```
Right-click on your database → Generate ERD
This will create a visual diagram showing:
- users → user_progress (relationship)
- users → user_submissions (relationship)
- cryptic_messages → user_submissions (relationship)
- email_templates → user_welcome_emails (relationship)
```

### 2. SQL Editor Enhancements - Better Query Writing

**Installation:**
1. Go to `Window` → `Preferences`
2. Navigate to `Database` → `SQL Editor`
3. Enable these features:
   - ✅ Auto-completion
   - ✅ Syntax highlighting
   - ✅ Query folding
   - ✅ Smart home/end
   - ✅ Show line numbers

**Additional Settings:**
```
SQL Editor → Code Completion:
- Enable auto-completion on typing
- Completion insert case: Lower case
- Auto-complete single proposals: ON

SQL Editor → SQL Formatting:
- Keyword case: UPPER CASE
- Identifier case: lower case
- Statement delimiter: semicolon
```

**Usage for Your Project:**
- Auto-complete table names (users, cryptic_messages, etc.)
- Syntax highlighting for complex queries
- Query folding for long analytics queries

### 3. Data Export/Import Tools - Bulk Operations

**Installation:**
1. Go to `Help` → `Install New Software...`
2. Click `Add...` button
3. Add Repository:
   - Name: `DBeaver Data Transfer`
   - Location: `https://dbeaver.io/update/latest/`
4. Select `Data Transfer Tools`
5. Install and restart

**Enhanced Export Templates for Your Service:**

#### Export Subscriber List:
```
Right-click users table → Export Data
Format: CSV
Columns: email, subscription_type, created_at, is_active
Filter: WHERE is_active = true
Output: /home/m/crypticmessages/exports/subscribers.csv
```

#### Import Your 273 Cryptic Messages:
```
Right-click cryptic_messages table → Import Data
Source: CSV file with your messages
Mapping: 
- week_number → week_number
- day_of_week → day_of_week
- title → title
- content → content
- difficulty_level → difficulty_level
```

#### Export Analytics Data:
```
Right-click weekly_challenge_stats view → Export Data
Format: Excel
Use for: Performance analysis reports
```

### 4. Performance Monitor - Track Query Performance

**Installation:**
1. Go to `Window` → `Preferences`
2. Navigate to `Database` → `Query Manager`
3. Enable:
   - ✅ Show query execution time
   - ✅ Log slow queries (> 1000ms)
   - ✅ Show query plan

**Additional Performance Tools:**
```
SQL Editor → Execution:
- Result set max size: 10000
- Query timeout: 30 seconds
- Fetch size: 1000

Database Navigator → Advanced:
- Enable connection pooling
- Pool size: 10 connections
```

**Performance Monitoring for Your API:**
```sql
-- Monitor your most used queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE query LIKE '%cryptic_messages%' 
   OR query LIKE '%user_submissions%'
   OR query LIKE '%users%'
ORDER BY total_time DESC
LIMIT 20;
```

## 🛠️ Additional Useful Plugins

### 5. Advanced SQL Console
**Installation:**
- `Help` → `Install New Software`
- Repository: `https://dbeaver.io/update/latest/`
- Select: `Advanced SQL Console`

**Features:**
- Multiple query tabs
- Query history
- Saved queries library
- Query bookmarks

### 6. Database Documentation Generator
**Installation:**
- Same repository as above
- Select: `Documentation Generator`

**Usage:**
- Generate documentation for your database schema
- Export table relationships
- Create database dictionary

## 📊 Verification Steps

After installing all plugins, verify functionality:

### Test ERD Generation:
```
1. Right-click theriddleroom database
2. Select "Generate ERD"
3. Should show visual diagram of your tables
4. Save as: cryptic_messages_schema.erd
```

### Test Enhanced SQL Editor:
```
1. Open new SQL Console
2. Type "SEL" - should auto-complete to "SELECT"
3. Type "users." - should show column suggestions
4. Query should have syntax highlighting
```

### Test Data Export:
```
1. Right-click users table
2. Export Data → CSV
3. Select few columns
4. Export to test file
5. Verify data integrity
```

### Test Performance Monitor:
```
1. Run a complex query on your data
2. Check Query Manager for execution time
3. View query plan for optimization suggestions
```

## 🎯 Plugin Configuration for Your Cryptic Message Service

### ERD Layout for Your Database:
```
users (center)
├── user_progress (right)
├── user_submissions (bottom-right)
└── user_welcome_emails (left)

cryptic_messages (bottom)
└── user_submissions (connects to users)

email_templates (top-left)
└── user_welcome_emails (connects to users)
```

### Saved Queries Library:
Create these commonly used queries:

1. **Daily Active Users**
```sql
SELECT COUNT(DISTINCT user_id) as active_users
FROM user_submissions 
WHERE DATE(created_at) = CURRENT_DATE;
```

2. **Weekly Revenue**
```sql
SELECT SUM(
    CASE subscription_type 
        WHEN 'monthly' THEN 19.99
        WHEN 'era' THEN 89.00 
        WHEN 'full' THEN 14.00
    END
) as weekly_revenue
FROM users 
WHERE created_at >= date_trunc('week', CURRENT_DATE);
```

3. **Challenge Success Rates**
```sql
SELECT 
    week_number,
    COUNT(*) as attempts,
    COUNT(CASE WHEN is_correct THEN 1 END) as successes,
    ROUND(COUNT(CASE WHEN is_correct THEN 1 END)::decimal / COUNT(*) * 100, 2) as success_rate
FROM user_submissions 
GROUP BY week_number 
ORDER BY week_number;
```

## ✅ Installation Complete!

Your DBeaver is now optimized for managing your cryptic message subscription service with:
- Visual database relationships
- Enhanced query writing
- Bulk data operations
- Performance monitoring
- Advanced analytics capabilities

Ready to manage your 273 cryptic messages and subscriber data efficiently! 🔐📊
