# DBeaver Extensions & Configuration for Cryptic Message Service
# Run these steps in DBeaver for optimal database management

## 1. Essential DBeaver Extensions to Install

### ERD (Entity Relationship Diagram) Plugin
- Help → Install New Software
- Add Repository: https://dbeaver.io/update/latest/
- Install: DBeaver ERD Plugin
- Use: Right-click database → Generate ERD

### SQL Editor Enhancements
- Preferences → Database → SQL Editor
- Enable: Auto-completion, Syntax highlighting, Query folding
- Set: Max result set size to 10000 for your analytics

### Data Export/Import Tools
- Enhanced CSV/Excel export for subscriber lists
- Bulk import for your 273 cryptic messages
- JSON export for API integration

## 2. Connection Optimization for Your PostgreSQL

### Connection Settings
- Host: localhost
- Port: 5432
- Database: theriddleroom
- Username: m
- Password: Prindle#$%10
- Driver: postgresql-42.7.1.jar

### Performance Settings
- Connection pool size: 10
- Query timeout: 30 seconds
- Auto-commit: false (for transactions)

### SSL Configuration
- SSL Mode: prefer
- SSL Factory: org.postgresql.ssl.DefaultJavaSSLFactory

## 3. Useful Scripts for Daily Operations

### Check Today's Scheduled Emails
```sql
SELECT 
    COUNT(*) as emails_scheduled_today,
    COUNT(CASE WHEN status = 'sent' THEN 1 END) as emails_sent,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as emails_pending
FROM user_welcome_emails 
WHERE DATE(scheduled_at) = CURRENT_DATE;
```

### Monitor Active Subscribers
```sql
SELECT 
    subscription_type,
    COUNT(*) as subscriber_count,
    COUNT(CASE WHEN is_active THEN 1 END) as active_count
FROM users 
GROUP BY subscription_type;
```

### Check Database Performance
```sql
SELECT 
    schemaname,
    tablename,
    n_live_tup as row_count,
    n_dead_tup as dead_rows,
    last_vacuum,
    last_analyze
FROM pg_stat_user_tables 
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
```

## 4. Data Export Templates

### Subscriber Export (for email campaigns)
- Table: users
- Columns: email, subscription_type, created_at, is_active
- Format: CSV
- Filter: is_active = true

### Challenge Performance Export
- View: weekly_challenge_stats
- Columns: week_number, title, success_rate_percent, avg_solve_time_minutes
- Format: Excel
- Use for: Difficulty adjustment analysis

### Revenue Report Export
- View: revenue_dashboard
- Columns: month, paid_subscribers, monthly_revenue
- Format: Excel
- Use for: Financial reporting

## 5. Backup & Maintenance

### Automated Backup Script
```sql
-- Create backup of user data
COPY (
    SELECT email, subscription_type, created_at, current_week, total_points
    FROM users u
    LEFT JOIN user_progress up ON u.id = up.user_id
    WHERE u.is_active = true
) TO '/tmp/user_backup.csv' WITH CSV HEADER;
```

### Database Maintenance
```sql
-- Analyze table statistics
ANALYZE users;
ANALYZE cryptic_messages;
ANALYZE user_submissions;

-- Vacuum dead rows
VACUUM ANALYZE user_welcome_emails;
```

## 6. Security Settings

### User Permissions
- Read-only user for analytics
- Admin user for data modification
- Service user for API connections

### Query Logging
- Enable slow query logging
- Monitor failed login attempts
- Track data export activities

This configuration optimizes DBeaver for managing your cryptic message subscription service efficiently! 🔐📊
