-- Custom Views for DBeaver - Cryptic Message Analytics
-- Create these views in your DBeaver for better data visualization

-- 1. User Journey Progress Dashboard
CREATE OR REPLACE VIEW user_journey_dashboard AS
SELECT 
    u.email,
    u.created_at as signup_date,
    u.subscription_type,
    up.current_week,
    up.total_solved,
    up.total_points,
    up.current_streak,
    ROUND((up.total_solved::decimal / 273) * 100, 2) as completion_percentage,
    CASE 
        WHEN up.current_streak >= 21 THEN 'Master Cryptographer'
        WHEN up.current_streak >= 14 THEN 'Advanced Solver'
        WHEN up.current_streak >= 7 THEN 'Regular Solver'
        ELSE 'Beginner'
    END as skill_level
FROM users u
LEFT JOIN user_progress up ON u.id = up.user_id
WHERE u.is_active = true;

-- 2. Weekly Challenge Performance
CREATE OR REPLACE VIEW weekly_challenge_stats AS
SELECT 
    cm.week_number,
    cm.day_of_week,
    cm.title,
    cm.difficulty_level,
    COUNT(us.id) as total_attempts,
    COUNT(CASE WHEN us.is_correct THEN 1 END) as correct_solutions,
    ROUND(
        COUNT(CASE WHEN us.is_correct THEN 1 END)::decimal / 
        NULLIF(COUNT(us.id), 0) * 100, 2
    ) as success_rate_percent,
    AVG(EXTRACT(EPOCH FROM (us.submitted_at - us.created_at))/60) as avg_solve_time_minutes
FROM cryptic_messages cm
LEFT JOIN user_submissions us ON cm.week_number = us.week_number
GROUP BY cm.id, cm.week_number, cm.day_of_week, cm.title, cm.difficulty_level
ORDER BY cm.week_number, 
    CASE cm.day_of_week 
        WHEN 'Sunday' THEN 1 
        WHEN 'Wednesday' THEN 2 
        WHEN 'Friday' THEN 3 
    END;

-- 3. Email Campaign Performance
CREATE OR REPLACE VIEW email_campaign_analytics AS
SELECT 
    et.template_name,
    et.email_sequence,
    et.subject_line,
    COUNT(uwe.id) as total_sent,
    COUNT(CASE WHEN uwe.status = 'delivered' THEN 1 END) as delivered,
    COUNT(CASE WHEN uwe.opened_at IS NOT NULL THEN 1 END) as opened,
    COUNT(CASE WHEN uwe.clicked_at IS NOT NULL THEN 1 END) as clicked,
    ROUND(
        COUNT(CASE WHEN uwe.opened_at IS NOT NULL THEN 1 END)::decimal / 
        NULLIF(COUNT(CASE WHEN uwe.status = 'delivered' THEN 1 END), 0) * 100, 2
    ) as open_rate_percent,
    ROUND(
        COUNT(CASE WHEN uwe.clicked_at IS NOT NULL THEN 1 END)::decimal / 
        NULLIF(COUNT(CASE WHEN uwe.opened_at IS NOT NULL THEN 1 END), 0) * 100, 2
    ) as click_through_rate_percent
FROM email_templates et
LEFT JOIN user_welcome_emails uwe ON et.id = uwe.template_id
GROUP BY et.id, et.template_name, et.email_sequence, et.subject_line
ORDER BY et.email_sequence;

-- 4. Revenue Analytics
CREATE OR REPLACE VIEW revenue_dashboard AS
SELECT 
    DATE_TRUNC('month', u.created_at) as month,
    COUNT(*) as total_signups,
    COUNT(CASE WHEN u.subscription_type != 'free_trial' THEN 1 END) as paid_subscribers,
    COUNT(CASE WHEN u.subscription_type = 'monthly' THEN 1 END) as monthly_subs,
    COUNT(CASE WHEN u.subscription_type = 'era' THEN 1 END) as era_subs,
    COUNT(CASE WHEN u.subscription_type = 'full' THEN 1 END) as full_journey_subs,
    -- Revenue calculations
    (COUNT(CASE WHEN u.subscription_type = 'monthly' THEN 1 END) * 19.99) +
    (COUNT(CASE WHEN u.subscription_type = 'era' THEN 1 END) * 89.00) +
    (COUNT(CASE WHEN u.subscription_type = 'full' THEN 1 END) * 294.00) as monthly_revenue
FROM users u
WHERE u.created_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', u.created_at)
ORDER BY month DESC;

-- 5. User Engagement Trends
CREATE OR REPLACE VIEW engagement_trends AS
SELECT 
    DATE(us.created_at) as submission_date,
    COUNT(DISTINCT us.user_id) as active_users,
    COUNT(us.id) as total_submissions,
    COUNT(CASE WHEN us.is_correct THEN 1 END) as correct_submissions,
    ROUND(AVG(us.points_earned), 2) as avg_points_per_submission,
    COUNT(CASE WHEN us.hint_used THEN 1 END) as hints_used
FROM user_submissions us
WHERE us.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(us.created_at)
ORDER BY submission_date DESC;
