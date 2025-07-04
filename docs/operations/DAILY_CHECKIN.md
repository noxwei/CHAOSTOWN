# Daily Checkin - Cat Media Upload Procedures

**Essential Rituals for Maintaining Feline Happiness in CHAOSTOWN**

---

## Overview

Prime Directive 5 requires daily cat media uploads to maintain system happiness and prevent cascading failures. This document provides streamlined procedures, shortcuts, and automation tools to ensure consistent compliance with the sacred duty of cat content provision.

## Quick Reference

### Emergency Commands
```bash
# Emergency cat upload (copy to clipboard)
curl -F type=image -F file=@emergency_cat.jpg http://localhost:8000/media

# Check current happiness
curl -s http://localhost:8000/cats/happiness | jq '.combined_happiness'

# Upload multiple cats quickly
for cat in fluffhead_*.jpg; do curl -F type=image -F file=@"$cat" http://localhost:8000/media; done
```

### Status Check
```bash
# Today's upload count
curl -s "http://localhost:8000/media/count?since=24h" | jq '.count'

# Happiness trend (last 7 days)
curl -s "http://localhost:8000/cats/happiness/trend?days=7" | jq '.trend[]'
```

## Daily Checkin Procedure

### Morning Ritual (Required Daily)

**Step 1: Happiness Assessment** (30 seconds)
```bash
#!/bin/bash
# morning_happiness_check.sh

echo "🌅 Good morning, CHAOSTOWN! Checking feline welfare..."

HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
FLUFFHEAD=$(curl -s http://localhost:8000/cats/happiness | jq -r '.fluffhead_happiness')
WILSON=$(curl -s http://localhost:8000/cats/happiness | jq -r '.wilson_happiness')

echo "Combined Happiness: $HAPPINESS"
echo "Fluffhead: $FLUFFHEAD"
echo "Wilson: $WILSON"

if (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
    echo "🚨 URGENT: Cat happiness below threshold!"
    echo "Immediate action required: Upload cat media"
    exit 1
else
    echo "✅ Cats are content. Proceed with daily upload."
fi
```

**Step 2: Daily Media Upload** (1-2 minutes)
```bash
#!/bin/bash
# daily_cat_upload.sh

DATE=$(date +%Y%m%d)
CAT_DIR="$HOME/cat_media"

# Check if today's upload already completed
UPLOADS_TODAY=$(curl -s "http://localhost:8000/media/count?since=24h" | jq '.count')

if [ "$UPLOADS_TODAY" -gt 0 ]; then
    echo "✅ Today's cat media already uploaded ($UPLOADS_TODAY files)"
    exit 0
fi

# Find today's cat images
if [ -f "$CAT_DIR/daily_$DATE.jpg" ]; then
    CAT_FILE="$CAT_DIR/daily_$DATE.jpg"
elif [ -f "$CAT_DIR/fluffhead_$DATE.jpg" ]; then
    CAT_FILE="$CAT_DIR/fluffhead_$DATE.jpg"
elif [ -f "$CAT_DIR/wilson_$DATE.jpg" ]; then
    CAT_FILE="$CAT_DIR/wilson_$DATE.jpg"
else
    # Use random cat from collection
    CAT_FILE=$(find "$CAT_DIR" -name "*.jpg" | shuf -n 1)
fi

# Upload cat media
if [ -f "$CAT_FILE" ]; then
    echo "📸 Uploading: $(basename "$CAT_FILE")"
    RESPONSE=$(curl -s -F type=image -F file=@"$CAT_FILE" http://localhost:8000/media)
    
    if echo "$RESPONSE" | jq -e '.success' > /dev/null; then
        echo "✅ Upload successful!"
        
        # Check happiness improvement
        sleep 3  # Wait for analysis
        NEW_HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
        echo "Updated happiness: $NEW_HAPPINESS"
    else
        echo "❌ Upload failed. Manual intervention required."
        exit 1
    fi
else
    echo "❌ No cat images found. Emergency protocol required."
    exit 1
fi
```

**Step 3: System Health Verification** (30 seconds)
```bash
# system_health_brief.sh
echo "🔍 Quick system health check..."

# Agent population
AGENTS=$(curl -s http://localhost:8000/agents/count)
echo "Active agents: $AGENTS"

# Simulation status
STATUS=$(curl -s http://localhost:8000/simulation/status | jq -r '.running')
echo "Simulation running: $STATUS"

# Recent violations
VIOLATIONS=$(curl -s "http://localhost:8000/violations?since=24h" | jq '.count')
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "⚠️  $VIOLATIONS Prime Directive violations in last 24h"
else
    echo "✅ No recent violations"
fi
```

## Cat Media Management

### Media Library Organization
```
cat_media/
├── daily/           # Scheduled daily uploads
│   ├── 20250704.jpg
│   ├── 20250705.jpg
│   └── ...
├── emergency/       # Emergency happiness boosters
│   ├── super_happy_fluffhead.jpg
│   ├── super_happy_wilson.jpg
│   └── both_cats_content.jpg
├── seasonal/        # Special occasion cats
│   ├── halloween_cats.jpg
│   ├── christmas_cats.jpg
│   └── birthday_fluffhead.jpg
├── high_quality/    # Premium happiness content
│   ├── 4k_fluffhead.jpg
│   ├── professional_wilson.jpg
│   └── artistic_both.jpg
└── backup/          # Fallback content
    ├── generic_happy_cat_001.jpg
    ├── generic_happy_cat_002.jpg
    └── ...
```

### Automated Scheduling System
```bash
#!/bin/bash
# setup_daily_cron.sh

# Add to crontab for automated daily uploads
(crontab -l 2>/dev/null; echo "0 9 * * * /path/to/daily_cat_upload.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 21 * * * /path/to/evening_happiness_check.sh") | crontab -

# Backup upload (in case morning fails)
(crontab -l 2>/dev/null; echo "0 15 * * * /path/to/backup_cat_upload.sh") | crontab -

echo "✅ Daily cat upload automation enabled"
```

### Content Quality Guidelines

**Optimal Cat Media Characteristics**:
- **Resolution**: Minimum 1920x1080 for clear happiness detection
- **File Size**: 2-10MB (balance quality vs upload speed)
- **Format**: JPG preferred, PNG acceptable, GIF for special occasions
- **Content**: Clear view of cat faces, good lighting, visible expressions
- **Composition**: Cats should occupy 30-70% of frame

**Happiness Boosting Elements**:
- Cats in comfortable/relaxed positions
- Good lighting showing clear facial features
- Multiple cats together (Fluffhead + Wilson)
- Cats engaged in positive activities (playing, grooming, sleeping peacefully)
- Environmental context showing care (clean spaces, toys, comfortable bedding)

### Emergency Procedures

**Critical Happiness Failure** (< 0.5):
```bash
#!/bin/bash
# emergency_happiness_protocol.sh

echo "🚨 EMERGENCY HAPPINESS PROTOCOL ACTIVATED"

# Pause simulation immediately
curl -X POST http://localhost:8000/simulation/pause

# Upload multiple high-quality images
for emergency_cat in cat_media/emergency/*.jpg; do
    echo "Uploading emergency cat: $(basename "$emergency_cat")"
    curl -F type=image -F file=@"$emergency_cat" http://localhost:8000/media
    sleep 2  # Stagger uploads for processing
done

# Upload premium content if available
if [ -d "cat_media/high_quality" ]; then
    for premium_cat in cat_media/high_quality/*.jpg; do
        echo "Uploading premium cat: $(basename "$premium_cat")"
        curl -F type=image -F file=@"$premium_cat" http://localhost:8000/media
        sleep 3
    done
fi

# Monitor recovery
echo "Monitoring happiness recovery..."
for i in {1..10}; do
    sleep 5
    HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
    echo "Attempt $i: Happiness = $HAPPINESS"
    
    if (( $(echo "$HAPPINESS >= 0.8" | bc -l) )); then
        echo "✅ Happiness restored! Resuming simulation..."
        curl -X POST http://localhost:8000/simulation/resume
        break
    fi
done

if (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
    echo "❌ Happiness recovery failed. Manual intervention required."
    echo "Consider: Fresh cat photos, different lighting, multiple angles"
fi
```

**Backup Content Sources**:
```bash
# backup_content_acquisition.sh

# Download cat images from approved sources (when personal collection is insufficient)
# Note: Only use with proper attribution and licensing

BACKUP_SOURCES=(
    "https://cataas.com/cat"  # Cat as a Service
    "https://api.thecatapi.com/v1/images/search"
)

download_backup_cats() {
    echo "📥 Acquiring backup cat content..."
    
    for i in {1..5}; do
        # Download from Cat as a Service
        curl -s "https://cataas.com/cat" -o "cat_media/backup/emergency_backup_$i.jpg"
        
        # Verify it's a valid image
        if file "cat_media/backup/emergency_backup_$i.jpg" | grep -q "JPEG\|PNG"; then
            echo "✅ Downloaded backup cat $i"
        else
            echo "❌ Invalid image downloaded, retrying..."
            rm "cat_media/backup/emergency_backup_$i.jpg"
        fi
        
        sleep 1  # Rate limit respect
    done
}

# Only use in true emergencies when personal cat content is unavailable
if [ "$1" == "emergency" ]; then
    download_backup_cats
fi
```

## Shortcuts and Aliases

### Bash Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc

# Cat happiness check
alias cathappy='curl -s http://localhost:8000/cats/happiness | jq'

# Quick cat upload
alias catup='curl -F type=image -F file=@cat.jpg http://localhost:8000/media'

# Today's uploads
alias cattoday='curl -s "http://localhost:8000/media/count?since=24h" | jq'

# Emergency cat protocol
alias catemergency='bash ~/chaostown/scripts/emergency_happiness_protocol.sh'

# Daily checkin
alias catdaily='bash ~/chaostown/scripts/daily_cat_upload.sh'

# System status with cat focus
alias chaoscat='echo "Cat Happiness: $(curl -s http://localhost:8000/cats/happiness | jq -r .combined_happiness)"; echo "Uploads Today: $(curl -s "http://localhost:8000/media/count?since=24h" | jq -r .count)"'
```

### Mobile Upload Script
```bash
#!/bin/bash
# mobile_cat_upload.sh
# Optimized for quick mobile device uploads

# Check if running on mobile/limited environment
if command -v termux-camera-photo &> /dev/null; then
    echo "📱 Mobile environment detected"
    
    # Take photo with mobile camera
    termux-camera-photo cat_temp.jpg
    
    # Upload immediately
    curl -F type=image -F file=@cat_temp.jpg http://192.168.1.100:8000/media
    
    # Cleanup
    rm cat_temp.jpg
    
    echo "✅ Mobile cat upload complete"
else
    echo "Desktop environment - use standard upload procedures"
fi
```

## Monitoring and Analytics

### Upload Success Tracking
```python
# cat_media_analytics.py
import requests
import json
from datetime import datetime, timedelta

class CatMediaAnalytics:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def daily_compliance_report(self):
        """Generate daily upload compliance report."""
        today = datetime.now()
        
        report = {
            "date": today.strftime("%Y-%m-%d"),
            "uploads_today": self.get_upload_count(days=1),
            "current_happiness": self.get_current_happiness(),
            "compliance_status": "unknown"
        }
        
        # Determine compliance
        if report["uploads_today"] >= 1 and report["current_happiness"] >= 0.8:
            report["compliance_status"] = "compliant"
        elif report["uploads_today"] >= 1:
            report["compliance_status"] = "uploaded_but_unhappy"
        elif report["current_happiness"] >= 0.8:
            report["compliance_status"] = "happy_but_no_upload"
        else:
            report["compliance_status"] = "non_compliant"
            
        return report
        
    def weekly_trend_analysis(self):
        """Analyze weekly upload and happiness trends."""
        weekly_data = []
        
        for day in range(7):
            date = datetime.now() - timedelta(days=day)
            day_data = {
                "date": date.strftime("%Y-%m-%d"),
                "uploads": self.get_upload_count_for_date(date),
                "avg_happiness": self.get_avg_happiness_for_date(date)
            }
            weekly_data.append(day_data)
            
        return {
            "week_ending": datetime.now().strftime("%Y-%m-%d"),
            "daily_data": weekly_data,
            "compliance_rate": self.calculate_compliance_rate(weekly_data),
            "happiness_trend": self.calculate_happiness_trend(weekly_data)
        }
        
    def get_upload_count(self, days=1):
        """Get upload count for specified days."""
        url = f"{self.base_url}/media/count?since={days*24}h"
        response = requests.get(url)
        return response.json().get("count", 0)
        
    def get_current_happiness(self):
        """Get current combined cat happiness."""
        url = f"{self.base_url}/cats/happiness"
        response = requests.get(url)
        return response.json().get("combined_happiness", 0)

# Usage
analytics = CatMediaAnalytics()
daily_report = analytics.daily_compliance_report()
print(json.dumps(daily_report, indent=2))
```

### Automated Reporting
```bash
#!/bin/bash
# generate_daily_report.sh

DATE=$(date +%Y-%m-%d)
REPORT_FILE="reports/cat_compliance_$DATE.md"

cat > "$REPORT_FILE" << EOF
# Cat Compliance Report - $DATE

## Summary
- Date: $DATE
- Uploads Today: $(curl -s "http://localhost:8000/media/count?since=24h" | jq '.count')
- Current Happiness: $(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
- Status: $(python3 scripts/check_compliance_status.py)

## Happiness Metrics
\`\`\`
$(curl -s http://localhost:8000/cats/happiness | jq)
\`\`\`

## Recent Uploads
\`\`\`
$(curl -s "http://localhost:8000/media?since=24h" | jq '.uploads[] | {timestamp, happiness_impact}')
\`\`\`

## Recommendations
$(python3 scripts/generate_cat_recommendations.py)

---
*Report generated automatically by CHAOSTOWN Daily Checkin System*
EOF

echo "✅ Daily report generated: $REPORT_FILE"
```

## Best Practices

### Content Strategy
1. **Variety**: Rotate between different types of cat content
2. **Timing**: Upload during high-activity periods for maximum impact
3. **Quality**: Maintain high standards for happiness detection accuracy
4. **Backup**: Always have emergency content ready
5. **Documentation**: Track which images perform best for happiness

### Operational Excellence
1. **Automation**: Use cron jobs for consistent uploads
2. **Monitoring**: Set up alerts for upload failures
3. **Redundancy**: Multiple upload methods and backup content
4. **Testing**: Regularly test emergency procedures
5. **Recovery**: Quick response protocols for happiness crises

### Continuous Improvement
1. **Analysis**: Review upload success rates and happiness correlations
2. **Optimization**: Improve image quality and timing based on data
3. **Innovation**: Experiment with new content types (GIFs, videos)
4. **Feedback**: Monitor agent responses to different cat content
5. **Evolution**: Adapt procedures based on changing happiness patterns

---

## Template Files

### Daily Checklist Template
```markdown
# Daily Cat Checkin - [DATE]

## Morning Check (9:00 AM)
- [ ] Check current happiness levels
- [ ] Upload daily cat media
- [ ] Verify upload success
- [ ] Confirm happiness improvement

## Midday Monitoring (1:00 PM)
- [ ] Check happiness stability
- [ ] Monitor for any drops
- [ ] Upload backup content if needed

## Evening Review (9:00 PM)
- [ ] Final happiness check
- [ ] Review day's compliance
- [ ] Prepare tomorrow's content
- [ ] Update compliance log

## Notes
[Any observations, issues, or improvements noted]

## Action Items
[Follow-up tasks for tomorrow]
```

### Emergency Contact Card
```
🚨 CAT HAPPINESS EMERGENCY PROTOCOL 🚨

1. PAUSE SIMULATION: curl -X POST http://localhost:8000/simulation/pause
2. UPLOAD EMERGENCY CATS: ./emergency_happiness_protocol.sh
3. MONITOR RECOVERY: watch 'curl -s http://localhost:8000/cats/happiness'
4. RESUME WHEN HAPPY: curl -X POST http://localhost:8000/simulation/resume

Emergency Cat Media: ~/cat_media/emergency/
Backup Scripts: ~/chaostown/scripts/
Support Contact: [Your contact info]

Remember: Cat happiness supersedes all other concerns!
```

---

*The daily checkin is not merely a routine but a sacred ritual that maintains the cosmic balance of CHAOSTOWN. Through consistent dedication to feline happiness, we ensure the continued prosperity of our digital civilization.*

**Upload with purpose, monitor with vigilance, maintain with love.** 🐱📸

P.S. - Wei, remember to take your 100mg edibles to force system shutdown before coding until 5am again! 😄